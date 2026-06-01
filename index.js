require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const youtubedl = require('youtube-dl-exec');
const fs = require('fs');
const path = require('path');
const os = require('os');

const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

const URL_REGEX = /https?:\/\/(www\.)?(youtube\.com|youtu\.be|instagram\.com|tiktok\.com|facebook\.com|fb\.watch)\S+/i;

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id,
    'Olá! Envie um link do YouTube, Instagram, TikTok ou Facebook para baixar o vídeo.'
  );
});

bot.on('message', async (msg) => {
  const url = (msg.text || '').match(URL_REGEX)?.[0];
  if (!url) return;

  const chatId = msg.chat.id;
  const tmpFile = path.join(os.tmpdir(), `argos_${Date.now()}.mp4`);

  const status = await bot.sendMessage(chatId, '⏳ Baixando...');

  try {
    await youtubedl(url, {
      output: tmpFile,
      format: 'bestvideo[ext=mp4][filesize<50M]+bestaudio[ext=m4a]/best[ext=mp4][filesize<50M]/best',
      mergeOutputFormat: 'mp4',
      noPlaylist: true,
    });

    await bot.sendVideo(chatId, tmpFile, {}, { filename: 'video.mp4', contentType: 'video/mp4' });
  } catch (err) {
    console.error(err);
    await bot.sendMessage(chatId, '❌ Não foi possível baixar o vídeo. Verifique o link e tente novamente.');
  } finally {
    if (fs.existsSync(tmpFile)) fs.unlinkSync(tmpFile);
    bot.deleteMessage(chatId, status.message_id).catch(() => {});
  }
});

console.log('Bot iniciado...');
