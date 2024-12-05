<script setup lang="ts">
import PencilSquareIcon from '@/components/icons/PencilSquareIcon.vue'
import TrashIcon from '@/components/icons/TrashIcon.vue'
import { ExecutableExists } from '@/wailsjs/go/main/App'
import { store } from '@/wailsjs/go/models'
import * as groupManager from '@/wailsjs/go/store/DriverGroupManager'
import { onBeforeMount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'
import DriverInputModal from './components/DriverInputModal.vue'

const $route = useRoute()

const $toast = useToast({ position: 'top-right' })

const notExistDrivers = ref<Array<string>>([])

const group = ref<store.DriverGroup>(
  new store.DriverGroup({
    type:
      store.DriverType[
        $route.query.type?.toString().toUpperCase() as keyof typeof store.DriverType
      ] ?? undefined,
    name: $route.query.name ?? '',
    drivers: []
  })
)

onBeforeMount(() => {
  if ($route.params.id) {
    groupManager.Get($route.params.id as string).then(g => {
      group.value = g
    })
  }
})

watch(group.value.drivers, newValue => {
  Promise.all(
    newValue.flatMap(d => ExecutableExists(d.path).then(exist => ({ id: d.id, exist: exist })))
  ).then(results => {
    notExistDrivers.value = results
      .map(result => (result.exist ? undefined : result.id))
      .filter(v => v !== undefined)
  })
})
</script>

<template>
  <form
    class="flex flex-col justify-center h-full max-w-full lg:max-w-2xl xl:max-w-4xl mx-auto gap-y-8 overflow-y-auto"
    autocomplete="off"
    @submit.prevent="
      () => {
        if (group.drivers.length == 0) {
          $toast.warning($t('toasts.addAtLeastOneDriver'))
        } else {
          ;(group.id == undefined ? groupManager.Add(group) : groupManager.Update(group))
            .then(() => $toast.success($t('toasts.updated')))
            .catch(reason => {
              $toast.error(reason)
            })
        }
      }
    "
  >
    <div class="flex gap-x-3">
      <div class="w-32">
        <label class="block mb-2 text-sm font-medium text-gray-900">
          {{ $t('driverForms.type') }}
        </label>
        <select
          name="type"
          v-model="group.type"
          class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
          required
        >
          <option v-for="type in store.DriverType" :key="type" :value="type">
            {{ $t(`driverCategories.${type}`) }}
          </option>
        </select>
      </div>

      <div class="flex-1">
        <label class="block mb-2 text-sm font-medium text-gray-900">
          {{ $t('driverForms.name') }}
        </label>
        <input
          type="text"
          name="name"
          v-model="group.name"
          class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
          required
        />
      </div>
    </div>

    <div class="flex flex-col gap-y-4">
      <label class="block text-sm font-medium text-gray-900">
        {{ $t('driverForms.driver') }}
      </label>

      <div class="max-h-[40vh] text-sm overflow-y-auto">
        <div class="grid grid-rows">
          <div class="grid grid-cols-10 gap-2 py-1.5 border-y">
            <div class="col-span-2">{{ $t('driverForms.name') }}</div>
            <div class="col-span-3">{{ $t('driverForms.path') }}</div>
            <div class="col-span-2">{{ $t('driverForms.argument') }}</div>
          </div>

          <div v-if="group.drivers.length == 0" class="py-1 text-center last:border-b">N/A</div>

          <div
            v-else
            v-for="(d, i) in group.drivers"
            :key="d.id"
            class="grid grid-cols-10 items-center gap-2 py-1.5 text-xs border-b"
          >
            <div class="col-span-2">
              <p class="truncate">
                {{ d.name }}
              </p>
            </div>
            <div class="col-span-3">
              <p class="font-mono truncate">
                {{ d.path }}
              </p>
            </div>
            <div class="col-span-2">
              <p class="truncate">
                {{ d.flags.join(', ') }}
              </p>
            </div>
            <div>
              <div class="flex gap-x-2">
                <button type="button" @click="$refs.inputModal?.show(d)">
                  <PencilSquareIcon></PencilSquareIcon>
                </button>
                <button type="button" @click="group.drivers.splice(i, 1)">
                  <TrashIcon></TrashIcon>
                </button>
              </div>
            </div>
          </div>
        </div>

        <p class="mt-1 text-xs font-light text-apple-green-800">
          {{ $t('driverForms.incompatibleForNewHelp') }}
        </p>
      </div>

      <div class="flex justify-end">
        <button
          type="button"
          class="px-3 py-1 text-sm font-medium text-white bg-powder-blue-800 hover:bg-powder-blue-600 rounded-lg"
          @click="$refs.inputModal?.show()"
        >
          +
        </button>
      </div>
    </div>

    <div class="flex h-8 gap-x-5">
      <button
        type="button"
        class="w-full text-sm font-medium text-white bg-gray-400 hover:bg-gray-300 rounded-lg"
        @click="$router.back()"
      >
        {{ $t('back') }}
      </button>

      <button
        type="submit"
        class="w-full text-sm font-medium text-white bg-half-baked-600 hover:bg-half-baked-500 rounded-lg"
      >
        {{ $t('save') }}
      </button>
    </div>
  </form>

  <DriverInputModal
    ref="inputModal"
    @submit="
      newDriver => {
        if (newDriver.id) {
          group.drivers = group.drivers.map(d => (d.id == newDriver.id ? newDriver : d))
        } else {
          group.drivers.push({
            ...newDriver,
            id: (group.drivers.length + 1).toString() // assign a temporary ID for editing
          })
        }

        $refs.inputModal?.hide()
      }
    "
  ></DriverInputModal>
</template>

<style scoped>
label:has(+ input:required, + select:required):after,
label:has(+ div > input:required):after {
  content: ' *';
  color: red;
}
</style>
