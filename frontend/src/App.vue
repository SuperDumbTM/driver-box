<script setup lang="ts">
import * as app_manager from '@/wailsjs/go/store/AppSettingManager'
import { onBeforeMount, type Component } from 'vue'
import { useI18n } from 'vue-i18n'
import type { RouteLocationRaw } from 'vue-router'
import FileExeIcon from './components/icons/FileExeIcon.vue'
import GearIcon from './components/icons/GearIcon.vue'
import HomeIcon from './components/icons/HomeIcon.vue'

const { locale } = useI18n()

const routes: Array<{ to: RouteLocationRaw; icon: Component }> = [
  { to: '/', icon: HomeIcon },
  { to: '/drivers', icon: FileExeIcon },
  { to: '/settings', icon: GearIcon }
]

onBeforeMount(() => {
  app_manager.Read().then(s => (locale.value = s.language))
})
</script>

<template>
  <div class="flex h-screen">
    <aside class="w-12">
      <div class="flex justify-center h-full px-1 py-3 overflow-y-auto bg-gray-50">
        <ul class="pt-3 space-y-3 font-medium">
          <li v-for="(link, i) in routes" :key="i">
            <RouterLink
              :to="link.to"
              class="flex items-center p-2 rounded-lg hover:bg-gray-200"
              activeClass="text-apple-green-900 bg-powder-blue-400"
            >
              <component :is="link.icon"></component>
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
