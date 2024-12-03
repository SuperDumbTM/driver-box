<script setup lang="ts">
import FileExeIcon from '@/components/icons/FileExeIcon.vue'
import GearIcon from '@/components/icons/GearIcon.vue'
import HomeIcon from '@/components/icons/HomeIcon.vue'
import * as app_manager from '@/wailsjs/go/store/AppSettingManager'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

app_manager.Read().then(s => (locale.value = s.language))
</script>

<template>
  <div class="flex h-screen">
    <aside class="w-12">
      <div class="flex justify-center h-full px-1 py-3 overflow-y-auto bg-gray-50">
        <ul class="pt-3 space-y-3 font-medium">
          <li>
            <RouterLink
              to="/"
              class="flex items-center p-2 rounded-lg hover:bg-gray-200"
              activeClass="text-apple-green-900 bg-powder-blue-400"
            >
              <HomeIcon></HomeIcon>
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/drivers"
              class="flex items-center p-2 rounded-lg hover:bg-gray-200"
              activeClass="text-apple-green-900 bg-powder-blue-400"
            >
              <FileExeIcon></FileExeIcon>
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/settings"
              class="flex items-center p-2 rounded-lg hover:bg-gray-200"
              activeClass="text-apple-green-900 bg-powder-blue-400"
            >
              <GearIcon></GearIcon>
            </RouterLink>
          </li>
        </ul>
      </div>
    </aside>

    <main class="w-full h-full p-3 overflow-x-hidden">
      <RouterView></RouterView>
    </main>
  </div>
</template>
