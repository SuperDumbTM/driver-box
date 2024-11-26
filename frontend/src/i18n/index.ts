import en from '@/i18n/en.json'
import zh_Hant_HK from '@/i18n/zh_Hant_HK.json'
import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  legacy: false,
  locale: 'zh_Hant_HK',
  messages: {
    en,
    zh_Hant_HK
  },
  fallbackLocale: 'en'
})

export { i18n }
