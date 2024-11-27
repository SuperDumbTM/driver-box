<script setup lang="ts">
import CopyIcon from '@/components/icons/CopyIcon.vue'
import PencilSquareIcon from '@/components/icons/PencilSquareIcon.vue'
import TrashIcon from '@/components/icons/TrashIcon.vue'
import InputModal from '@/views/driver/components/InputModal.vue'
import { store } from '@/wailsjs/go/models'
import * as manager from '@/wailsjs/go/store/DriverManager'
import { computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'vue-toast-notification'

const { t } = useI18n()

const $toast = useToast({ position: 'top-right' })

const driType = ref(store.DriverType.NETWORK)

const drivers = ref<Array<store.Driver>>([])

const notExistDrivers = ref<Array<string>>([])

const reordering = ref(false)

const driverOfType = computed(() => {
  return drivers.value?.filter(d => d.type == driType.value)
})

manager
  .Read()
  .then(d => (drivers.value = d))
  .catch(() => {
    $toast.error(t('toasts.readDriverFailed'))
  })

watch(drivers, (newValue, oldValue) => {
  if (newValue.length == oldValue.length) {
    return
  }

  Promise.all(
    newValue.map(d => manager.PathExist(d.id).then(exist => ({ id: d.id, exist: exist })))
  ).then(results => {
    notExistDrivers.value = results
      .map(result => (result.exist ? undefined : result.id))
      .filter(v => v !== undefined)
  })
})
</script>

<template>
  <div class="flex flex-col h-full gap-y-3">
    <ul class="flex flex-row gap-x-3 list-none text-center">
      <li class="flex-1" v-for="type in store.DriverType" :key="type">
        <a
          class="block px-4 py-3 text-xs leading-normal font-bold uppercase select-none shadow-lg rounded"
          :class="{
            'text-half-baked-600 bg-white': driType !== type,
            'text-white bg-half-baked-600': driType === type
          }"
          @click="driType = type"
        >
          {{ t(`driverCategories.${type}`) }}
        </a>
      </li>
    </ul>

    <div class="flex flex-col grow min-h-48 overflow-y-auto shadow-lg rounded">
      <table class="table-fixed text-sm text-left text-gray-500">
        <thead class="sticky top-0 text-xs text-gray-700 uppercase bg-gray-50">
          <tr>
            <th scope="col" class="px-4 py-4 text-nowrap">
              {{ $t('driverForms.name') }}
            </th>
            <th scope="col" class="px-4 py-4 text-nowrap">
              {{ $t('driverForms.path') }}
            </th>
            <th scope="col" class="sm:px-4 py-4 text-nowrap">
              {{ $t('driverForms.argument') }}
            </th>
            <th scope="col" class="px-4 py-4 text-nowrap">
              {{ $t('driverForms.action') }}
            </th>
          </tr>
        </thead>
        <tbody draggable="false">
          <tr
            v-for="(d, i) in driverOfType"
            :key="d.id"
            class="even:bg-half-baked-100"
            :draggable="reordering"
            @dragstart="
              event => {
                if (!reordering) {
                  return event.preventDefault()
                }

                event.dataTransfer!.setData('id', d.id)
                event.dataTransfer!.setData('position', i.toString())
              }
            "
            @dragover.prevent="
              event => {
                ;(event.target as HTMLTableCellElement)
                  .closest('tr')!
                  .classList.add('border-b', 'border-b-half-baked-700')
              }
            "
            @dragenter.prevent
            @dragleave="
              event => {
                ;(event.target as HTMLTableCellElement)
                  .closest('tr')!
                  .classList.remove('border-b', 'border-b-half-baked-700')
              }
            "
            @drop="
              async event => {
                ;(event.target as HTMLTableCellElement)
                  .closest('tr')!
                  .classList.remove(
                    'border-b',
                    'border-b-half-baked-700',
                    'border-t',
                    'border-t-half-baked-700'
                  )

                // async functuion will cause event.dataTransfer lost data
                const sourceId = event.dataTransfer!.getData('id')
                const sourcePosition = event.dataTransfer!.getData('position')

                manager.IndexOf(d.id).then(targetIndex => {
                  if (parseInt(sourcePosition) <= i) {
                    // aligning MoveBehind's logic and UI draging's logic
                    targetIndex -= 1
                  }

                  manager.MoveBehind(sourceId, targetIndex).then(result => {
                    drivers = result
                  })
                })
              }
            "
          >
            <th scope="row" class="px-4 py-2 text-sm font-medium text-gray-900 whitespace-nowrap">
              {{ d.name }}
            </th>
            <td
              class="px-4 py-2 min-w-28 text-xs break-all font-mono"
              :class="[notExistDrivers.includes(d.id) ? 'text-rose-500 font-medium' : 'font-light']"
            >
              {{ d.path }}
            </td>
            <td class="px-4 py-2 text-xs">{{ d.flags }}</td>
            <td class="px-4 py-2">
              <div class="flex gap-x-1.5">
                <button
                  class="p-1 text-sm font-medium bg-gray-200 rounded"
                  @click="$refs.inputModal?.show(d)"
                >
                  <PencilSquareIcon></PencilSquareIcon>
                </button>

                <button
                  class="p-1 text-sm font-medium bg-gray-200 rounded"
                  @click="
                    manager.Remove(d).then(() =>
                      manager.Read().then(d => {
                        drivers = d
                      })
                    )
                  "
                >
                  <TrashIcon></TrashIcon>
                </button>

                <button
                  class="p-1 text-sm font-medium bg-gray-200 rounded"
                  @click="
                    manager.Add(d).then(() =>
                      manager.Read().then(d => {
                        drivers = d
                      })
                    )
                  "
                >
                  <CopyIcon></CopyIcon>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex justify-end gap-x-3">
      <button
        v-show="driverOfType.length > 1"
        type="button"
        class="h-8 px-3 text-white text-sm focus:outline-none rounded"
        :class="[
          reordering
            ? 'bg-apple-green-800 hover:bg-apple-green-700  animate-blink-75'
            : 'bg-[#D9BD68] hover:bg-[#E5D195]'
        ]"
        @click="reordering = !reordering"
      >
        {{ reordering ? $t('driverForms.view') : $t('driverForms.order') }}
      </button>

      <button
        type="button"
        class="h-8 px-3 text-white text-sm focus:outline-none enabled:bg-powder-blue-800 disabled:bg-powder-blue-500 enabled:hover:bg-powder-blue-700 rounded"
        @click="$refs.inputModal?.show({ type: driType })"
        :disabled="reordering"
      >
        {{ $t('driverForms.create') }}
      </button>
    </div>

    <InputModal
      :drivers="drivers ?? []"
      ref="inputModal"
      @submit="
        async dri => {
          try {
            if (dri.id) {
              await manager.Update(dri)
            } else {
              await manager.Add(dri)
            }
          } catch (error: any) {
            $toast.error(error.toString())
            return
          }

          manager.Read().then(d => {
            drivers = d
            $refs.inputModal?.hide()
          })
        }
      "
    ></InputModal>
  </div>
</template>
