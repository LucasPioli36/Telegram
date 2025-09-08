from dotenv import load_dotenv
import os
import gspread
from datetime import datetime
from telegram import Update
from google.oauth2.service_account import Credentials
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
load_dotenv()

# Configuración de Google Sheets
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

import json

# Obtener credenciales desde variables de entorno
credentials_json = os.getenv("GOOGLE_CREDENTIALS")
if credentials_json:
    credentials_dict = json.loads(credentials_json)
    creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
else:
    # Fallback para desarrollo local
    creds = Credentials.from_service_account_file("credentiasCuentaServicioGastosFamiliares.json", scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_key("1TIFqRmN_gl0dTnSn8W040wpRPOxqskfXfhsjVtS2NnM").sheet1
print("Conectado a Google Sheets:", sheet.title)


async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Emi te amo")

def is_user_allowed(user_id):
    allowed_users = os.getenv("ALLOWED_USERS", "").split(",")
    return str(user_id) in allowed_users

async def add_gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Función agregar_gasto ejecutada")
    # Obtener el mensaje del usuario
    mensaje = update.message.text
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("❌ No tienes permisos para usar este bot")
        return
    partes = mensaje.split(' ', 1)  # Divide en 2 partes: comando y resto
    
    if len(partes) < 2:
        await update.message.reply_text("Formato: /gasto 1500 comida")
        return
    
    try:
        monto = float(partes[1].split()[0])
        categoria = partes[1].split()[1] if len(partes[1].split()) > 1 else "otros"
        
        # Agregar a Google Sheets
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        usuario = update.effective_user.first_name
        
        sheet.append_row([fecha, "Gasto", monto, "UYU", categoria, usuario])
        ##print(f"Agregando fila: {[fecha, 'Gasto', monto, "UYU",categoria, usuario]}")
        await update.message.reply_text(f"✅ Gasto registrado: ${monto} en {categoria}")
        
    except ValueError:
        await update.message.reply_text("❌ Error: El monto debe ser un número")




async def add_ingreso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtener el mensaje del usuario
    mensaje = update.message.text
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("❌ No tienes permisos para usar este bot")
        return
    partes = mensaje.split(' ', 1)  # Divide en 2 partes: comando y resto
    
    if len(partes) < 2:
        await update.message.reply_text("Formato: /ingreso 50000 salario")
        return
    
    try:
        monto = float(partes[1].split()[0])
        categoria = partes[1].split()[1] if len(partes[1].split()) > 1 else "otros"
        
        # Agregar a Google Sheets
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        usuario = update.effective_user.first_name
        
        sheet.append_row([fecha, "Ingreso", monto, "UYU", categoria, usuario])
        ##print(f"Agregando fila: {[fecha, 'Ingreso', monto, "UYU",categoria, usuario]}")
        
        await update.message.reply_text(f"✅ Ingreso registrado: ${monto} de {categoria}")
        
    except ValueError:
        await update.message.reply_text("❌ Error: El monto debe ser un número")
        
async def add_gasto_usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtener el mensaje del usuario
    mensaje = update.message.text
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("❌ No tienes permisos para usar este bot")
        return
    partes = mensaje.split(' ', 1)  # Divide en 2 partes: comando y resto
    
    if len(partes) < 2:
        await update.message.reply_text("Formato: /gastoUSD 50 comida")
        return
    
    try:
        monto = float(partes[1].split()[0])
        categoria = partes[1].split()[1] if len(partes[1].split()) > 1 else "otros"
        
        # Agregar a Google Sheets
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        usuario = update.effective_user.first_name
        
        sheet.append_row([fecha, "Gasto", monto, "USD", categoria, usuario])
        ##print(f"Agregando fila: {[fecha, 'Gasto USD', monto, "USD",categoria, usuario]}")
        
        await update.message.reply_text(f"✅ Gasto en USD registrado: ${monto} en {categoria}")
        
    except ValueError:
        await update.message.reply_text("❌ Error: El monto debe ser un número")

async def add_ingreso_usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtener el mensaje del usuario
    mensaje = update.message.text
    if not is_user_allowed(update.effective_user.id):
        await update.message.reply_text("❌ No tienes permisos para usar este bot")
        return
    partes = mensaje.split(' ', 1)  # Divide en 2 partes: comando y resto
    
    if len(partes) < 2:
        await update.message.reply_text("Formato: /ingresoUSD 1000 freelance")
        return
    
    try:
        monto = float(partes[1].split()[0])
        categoria = partes[1].split()[1] if len(partes[1].split()) > 1 else "otros"
        
        # Agregar a Google Sheets
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        usuario = update.effective_user.first_name
        
        sheet.append_row([fecha, "Ingreso", monto, "USD", categoria, usuario])
        ##print(f"Agregando fila: {[fecha, 'Ingreso USD', monto, "USD",categoria, usuario]}")
        
        await update.message.reply_text(f"✅ Ingreso en USD registrado: ${monto} de {categoria}")
        
    except ValueError:
        await update.message.reply_text("❌ Error: El monto debe ser un número")


app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build() ## comando para crear aplicacion
app.add_handler(CommandHandler("start", say_hello))



app.add_handler(CommandHandler("gasto", add_gasto))
app.add_handler(CommandHandler("ingreso", add_ingreso))
app.add_handler(CommandHandler("gastoUSD", add_gasto_usd))
app.add_handler(CommandHandler("ingresoUSD", add_ingreso_usd))
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


