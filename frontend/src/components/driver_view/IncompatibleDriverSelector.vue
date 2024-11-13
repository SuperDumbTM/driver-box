<script setup lang="ts">
import type { store } from '@/wailsjs/go/models'
import { computed, ref, useTemplateRef } from 'vue'

const props = defineProps<{ options?: Array<store.Driver> }>()

const value = defineModel<Array<string>>({ default: [] })

const visible = ref(false)

const selectUl = useTemplateRef('select-box')

const search = ref('')

const badgeStyle = {
  network: {
    text: '網絡',
    classes: 'bg-blue-100'
  },
  display: {
    text: '顯示',
    classes: 'bg-green-100'
  },
  miscellaneous: {
    text: '其他',
    classes: 'bg-gray-100'
  }
}

const showOptions = computed(() => {
  if (search.value === '') {
    return props.options
  } else {
    return props.options?.filter(dri => dri.name.includes(search.value))
  }
})

const handleClickOutside = (event: Event) => {
  if (visible.value === false) {
    return
  }

  if (!selectUl.value?.parentNode?.contains((event.target as HTMLElement)?.parentNode)) {
    visible.value = false
    document.removeEventListener('click', handleClickOutside)
  }
}

function addClickOutsideHandler() {
  document.addEventListener('click', handleClickOutside)
}
</script>

<template>
  <div class="relative w-max">
    <button
      type="button"
      class="w-20 me-1 px-2 py-1.5 text-white text-sm font-semibold rounded border-none bg-half-baked-600 hover:bg-half-baked-500"
      @click="
        () => {
          visible = !visible
          addClickOutsideHandler()
        }
      "
    >
      選擇 ({{ value.length }})
    </button>

    <button
      type="button"
      class="mx-1 px-2 py-1 text-white text-xs rounded border-none bg-apple-green-700 hover:bg-apple-green-600"
      @click="
        () => {
          value = props.options?.map(dri => dri.id) ?? []
        }
      "
    >
      全選
    </button>

    <button
      type="button"
      class="mx-1 px-2 py-1 text-white text-xs rounded border-none bg-red-400 hover:bg-red-300"
      @click="
        () => {
          value = []
        }
      "
    >
      取消選擇
    </button>

    <ul
      ref="select-box"
      class="absolute top-0 left-20 block min-w-full w-max max-h-52 p-1.5 z-20 overflow-auto bg-white shadow-2xl rounded-lg"
      :class="{ hidden: !visible }"
    >
      <li class="mb-2">
        <input
          v-model="search"
          placeholder="搜尋..."
          class="px-4 py-2 w-full text-black text-sm border-none rounded outline-apple-green-600 bg-gray-50"
        />
      </li>

      <template v-for="dri in showOptions" :key="dri.id">
        <li class="py-2.5 px-4 text-sm">
          <label class="flex item-center w-full select-none cursor-pointer">
            <input type="checkbox" :value="dri.id" v-model="value" class="me-1.5" />
            <span class="mx-1 px-1.5 py-0.5 text-xs rounded" :class="badgeStyle[dri.type]?.classes">
              {{ badgeStyle[dri.type]?.text }}
            </span>
            {{ dri.name }}
          </label>
        </li>
      </template>
    </ul>
  </div>
</template>
