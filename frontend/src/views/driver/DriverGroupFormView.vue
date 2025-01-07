<script setup lang="ts">
import ArrowExpandVerticalIcon from '@/components/icons/ArrowExpandVerticalIcon.vue'
import OneTwoThreeIcon from '@/components/icons/OneTwoThreeIcon.vue'
import PencilSquareIcon from '@/components/icons/PencilSquareIcon.vue'
import TrashIcon from '@/components/icons/TrashIcon.vue'
import { ExecutableExists } from '@/wailsjs/go/main/App'
import { store } from '@/wailsjs/go/models'
import * as groupManager from '@/wailsjs/go/store/DriverGroupManager'
import { onBeforeMount, ref, useTemplateRef, watch } from 'vue'
import { onBeforeRouteLeave, useRoute } from 'vue-router'
import { useToast } from 'vue-toast-notification'
import DriverInputModal from './components/DriverInputModal.vue'
import UnsaveConfirmModal from './components/UnsaveConfirmModal.vue'

const $route = useRoute()

const $toast = useToast({ position: 'top-right' })

const questionModal = useTemplateRef('questionModal')

const modified = ref(false)

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

onBeforeRouteLeave((to, from, next) => {
  if (modified.value) {
    questionModal.value?.show(answer => {
      next(answer == 'yes')
    })
  } else {
    next(true)
  }
})

watch(group.value, () => (modified.value = true), { once: true })

watch(group.value.drivers, newValue => {
  if (!modified.value) {
    modified.value = true
  }

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
          $toast.warning($t('toast.addAtLeastOneDriver'))
        } else {
          ;(group.id == undefined ? groupManager.Add(group) : groupManager.Update(group))
            .then(() => {
              modified = false
              $toast.success($t('toast.updated'))
            })
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
          {{ $t('driverForm.type') }}
        </label>
        <select name="type" v-model="group.type" class="w-full p-1.5 text-sm shadow-sm" required>
          <option v-for="type in store.DriverType" :key="type" :value="type">
            {{ $t(`driverCatetory.${type}`) }}
          </option>
        </select>
      </div>

      <div class="flex-1">
        <label class="block mb-2 text-sm font-medium text-gray-900">
          {{ $t('driverForm.name') }}
        </label>
        <input
          type="text"
          name="name"
          v-model="group.name"
          class="w-full p-1.5 text-sm shadow-sm"
          required
        />
      </div>
    </div>

    <div class="flex flex-col gap-y-4">
      <label class="block text-sm font-medium text-gray-900">
        {{ $t('driverForm.driver') }}
      </label>

      <div class="max-h-[40vh] text-sm overflow-y-auto">
        <div class="grid grid-rows">
          <div class="grid grid-cols-10 gap-2 py-1.5 border-y">
            <div class="col-span-2">{{ $t('driverForm.name') }}</div>
            <div class="col-span-3">{{ $t('driverForm.path') }}</div>
            <div class="col-span-2">{{ $t('driverForm.argument') }}</div>
            <div class="col-span-2">{{ $t('driverForm.otherSetting') }}</div>
          </div>

          <div v-if="group.drivers.length == 0" class="py-1 text-center last:border-b">N/A</div>

          <div
            v-else
            v-for="(d, i) in group.drivers"
            :key="d.id"
            class="grid grid-cols-10 items-center gap-2 py-1.5 text-xs border-b"
          >
            <div class="col-span-2">
              <p class="break-all line-clamp-2">
                {{ d.name }}
              </p>
            </div>

            <div class="col-span-3">
              <p class="font-mono break-all line-clamp-2">
                {{ d.path }}
              </p>
            </div>

            <div class="col-span-2">
              <p class="break-all line-clamp-2">
                {{ d.flags.join(', ') }}
              </p>
            </div>

            <div class="flex col-span-2 gap-x-1">
              <span
                v-show="d.incompatibles.length > 0"
                class="inline-block p-0.5 max-h-5 bg-yellow-300 rounded-sm"
                :title="$t('driverForm.incompatibleWith')"
              >
                <ArrowExpandVerticalIcon></ArrowExpandVerticalIcon>
              </span>

              <span
                v-show="d.allowRtCodes.length > 0"
                class="inline-block p-0.5 max-h-5 bg-blue-300 rounded-sm"
                :title="$t('driverForm.allowedExitCode')"
              >
                <OneTwoThreeIcon></OneTwoThreeIcon>
              </span>
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

        <p class="hint-text">
          {{ $t('driverForm.incompatibleForNewHelp') }}
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
        {{ $t('common.back') }}
      </button>

      <button
        type="submit"
        class="w-full text-sm font-medium text-white bg-half-baked-600 hover:bg-half-baked-500 rounded-lg"
      >
        {{ $t('common.save') }}
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

  <UnsaveConfirmModal ref="questionModal"></UnsaveConfirmModal>
</template>

<style scoped>
label:has(+ input:required, + select:required):after,
label:has(+ div > input:required):after {
  content: ' *';
  color: red;
}
</style>
