<script setup lang="ts">
import type { store } from '@/wailsjs/go/models'
import { computed, ref, useTemplateRef } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps<{ options?: Array<store.Driver> }>()

const value = defineModel<Array<string>>({ default: [] })

const { t } = useI18n()

const visible = ref(false)

const selectUl = useTemplateRef('select-box')

const search = ref('')

const badgeStyle = {
  network: {
    text: t('driverForms.network'),
    classes: 'bg-blue-100'
  },
  display: {
    text: t('driverForms.display'),
    classes: 'bg-green-100'
  },
  miscellaneous: {
    text: t('driverForms.miscellaneous'),
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
      class="w-24 me-1 px-2 py-1.5 text-white text-sm font-semibold rounded border-none bg-half-baked-600 hover:bg-half-baked-500"
      @click="
        () => {
          visible = !visible
          addClickOutsideHandler()
        }
      "
    >
      {{ $t('driverForms.selectWithCount', { count: value.length }) }}
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
      {{ $t('driverForms.selectAll') }}
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
      {{ $t('driverForms.selectNothing') }}
    </button>

    <ul
      ref="select-box"
      class="absolute top-0 left-20 block w-60 max-h-52 p-1.5 z-20 overflow-auto bg-white shadow-2xl rounded-lg"
      :class="{ hidden: !visible }"
    >
      <li class="mb-2">
        <input
          v-model="search"
          :placeholder="$t('driverForms.search')"
          class="px-4 py-2 w-full text-black text-sm border-none rounded outline-apple-green-600 bg-gray-50"
        />
      </li>

      <li class="py-2.5 px-4 text-sm" v-show="search === ''">
        <label class="flex item-center w-full select-none cursor-pointer">
          <input type="checkbox" value="set_password" v-model="value" class="me-1.5" />
          <span class="mx-1 px-1.5 py-0.5 text-xs bg-orange-200 rounded">
            {{ $t('driverForms.default') }}
          </span>
          {{ $t('installOptions.setPassword') }}
        </label>
      </li>

      <li class="py-2.5 px-4 text-sm" v-show="search === ''">
        <label class="flex item-center w-full select-none cursor-pointer">
          <input type="checkbox" value="create_partition" v-model="value" class="me-1.5" />
          <span class="mx-1 px-1.5 py-0.5 text-xs bg-orange-200 rounded">
            {{ $t('driverForms.default') }}
          </span>
          {{ $t('installOptions.createPartition') }}
        </label>
      </li>

      <template v-for="dri in showOptions" :key="dri.id">
        <li class="py-2.5 px-4 text-sm">
          <label class="flex items-center w-full select-none cursor-pointer">
            <input type="checkbox" :value="dri.id" v-model="value" class="me-1.5" />
            <span
              class="content-center mx-1 px-1.5 h-5 text-xs text-nowrap rounded"
              :class="badgeStyle[dri.type]?.classes"
            >
              {{ badgeStyle[dri.type]?.text }}
            </span>
            <span class="line-clamp-3">
              {{ dri.name }}
            </span>
          </label>
        </li>
      </template>
    </ul>
  </div>
</template>
