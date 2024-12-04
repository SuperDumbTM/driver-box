<script setup lang="ts">
import ArrowExpandVerticalIcon from '@/components/icons/ArrowExpandVerticalIcon.vue'
import CopyIcon from '@/components/icons/CopyIcon.vue'
import OneTwoThreeIcon from '@/components/icons/OneTwoThreeIcon.vue'
import PencilSquareIcon from '@/components/icons/PencilSquareIcon.vue'
import TrashIcon from '@/components/icons/TrashIcon.vue'
import { store } from '@/wailsjs/go/models'
import * as groupManger from '@/wailsjs/go/store/DriverGroupManager'
import { computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toast-notification'
import DriverTypeBadget from './components/DriverTypeBadget.vue'

const { t } = useI18n()

const $router = useRouter()

const $route = useRoute()

const $toast = useToast({ position: 'top-right' })

const driverType = ref(
  store.DriverType[$route.query.type?.toString().toUpperCase() as keyof typeof store.DriverType] ??
    store.DriverType.NETWORK
)

const groups = ref<Array<store.DriverGroup>>([])

const notExistDrivers = ref<Array<string>>([])

const reordering = ref(false)

const driverOfType = computed(() => {
  return groups.value?.filter(d => d.type == driverType.value)
})

groupManger
  .Read()
  .then(g => (groups.value = g))
  .catch(() => {
    $toast.error(t('toasts.readDriverFailed'))
  })

watch(groups, (newValue, oldValue) => {
  if (newValue.length == oldValue.length) {
    return
  }

  Promise.all(
    newValue.flatMap(g =>
      g.drivers.flatMap(d =>
        groupManger.PathExist(g.id, d.id).then(exist => ({ id: d.id, exist: exist }))
      )
    )
  ).then(results => {
    notExistDrivers.value = results
      .map(result => (result.exist ? undefined : result.id))
      .filter(v => v !== undefined)
  })
})

watch(driverType, newValue => {
  $router.replace({ path: '/drivers', query: { type: newValue } })
})
</script>

<template>
  <div class="flex flex-col h-full gap-y-2">
    <ul class="flex flex-row gap-x-3 list-none text-center">
      <li class="flex-1" v-for="type in store.DriverType" :key="type">
        <a
          class="block px-4 py-3 text-xs leading-normal font-bold uppercase select-none shadow-lg rounded"
          :class="{
            'text-half-baked-600 bg-white': driverType !== type,
            'text-white bg-half-baked-600': driverType === type
          }"
          @click="driverType = type"
        >
          {{ t(`driverCategories.${type}`) }}
        </a>
      </li>
    </ul>

    <div class="flex flex-col grow py-2 min-h-48 overflow-y-scroll shadow-lg rounded">
      <div
        v-for="(g, i) in groups.filter(g => g.type == driverType)"
        :key="g.id"
        class="driver-card m-1 px-2 py-1 border border-gray-200 rounded-lg shadow"
        :class="reordering ? 'select-none cursor-pointer' : ''"
        @dragstart="
          event => {
            if (!reordering) {
              return event.preventDefault()
            }

            event.dataTransfer!.setData('id', g.id)
            event.dataTransfer!.setData('position', i.toString())
          }
        "
        @dragover.prevent="
          event => {
            ;(event.target as HTMLDivElement)
              .closest('.driver-card')!
              .classList.add('border-b-2', 'border-b-half-baked-700')
          }
        "
        @dragenter.prevent
        @dragleave="
          event => {
            ;(event.target as HTMLDivElement)
              .closest('.driver-card')!
              .classList.remove('border-b-2', 'border-b-half-baked-700')
          }
        "
        @drop="
          async event => {
            ;(event.target as HTMLDivElement)
              .closest('.driver-card')!
              .classList.remove('border-b-2', 'border-b-half-baked-700')

            // async functuion will cause event.dataTransfer lost data
            const sourceId = event.dataTransfer!.getData('id')
            const sourcePosition = event.dataTransfer!.getData('position')

            groupManger.IndexOf(g.id).then(targetIndex => {
              if (parseInt(sourcePosition) <= i) {
                // aligning MoveBehind's logic and UI draging's logic
                targetIndex -= 1
              }

              groupManger.MoveBehind(sourceId, targetIndex).then(result => {
                groups = result
              })
            })
          }
        "
        :draggable="reordering"
      >
        <div class="flex justify-between">
          <p class="my-1 truncate oveflow-x-hidden">
            <DriverTypeBadget :type="g.type"></DriverTypeBadget>
            <span>{{ g.name }}</span>
          </p>

          <div class="flex gap-x-1.5 py-1">
            <RouterLink :to="`/drivers/edit/${g.id}`" class="p-1 bg-gray-200 rounded">
              <PencilSquareIcon></PencilSquareIcon>
            </RouterLink>

            <button
              class="p-1 bg-gray-200 rounded"
              @click="
                () => {
                  groupManger.Add(g).then(() => {
                    groupManger.Read().then(g => {
                      groups = g
                    })
                  })
                }
              "
            >
              <CopyIcon></CopyIcon>
            </button>

            <button
              class="p-1 bg-gray-200 rounded"
              @click="
                () => {
                  groupManger.Remove(g.id).then(() => {
                    groupManger.Read().then(g => {
                      groups = g
                    })
                  })
                }
              "
            >
              <TrashIcon></TrashIcon>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-12 gap-1 py-1 text-xs bg-gray-100">
          <div class="col-span-2 lg:col-span-3 font-medium">{{ $t('driverForms.name') }}</div>
          <div class="col-span-5 lg:col-span-5 font-medium">{{ $t('driverForms.path') }}</div>
          <div class="col-span-3 lg:col-span-3 font-medium">{{ $t('driverForms.argument') }}</div>
          <div class="col-span-2 lg:col-span-1 font-medium">{{ '其他設定' }}</div>
        </div>

        <div v-for="d in g.drivers" :key="d.id" class="grid grid-cols-12 gap-1 py-1 text-xs">
          <div class="col-span-2 lg:col-span-3 break-all line-clamp-2">
            {{ d.name }}
          </div>

          <div
            class="col-span-5 lg:col-span-5 break-all line-clamp-2"
            :class="{ 'text-red-600': notExistDrivers.includes(d.id) }"
          >
            {{ d.path }}
          </div>

          <div class="col-span-3 lg:col-span-3 break-all line-clamp-2">
            {{ d.flags }}
          </div>

          <div class="flex col-span-2 lg:col-span-1 gap-x-1">
            <span
              v-show="d.incompatibles.length > 0"
              class="inline-block p-0.5 max-h-5 bg-yellow-300 rounded-sm"
              :title="$t('driverForms.incompatibleWith')"
            >
              <ArrowExpandVerticalIcon></ArrowExpandVerticalIcon>
            </span>

            <span
              v-show="d.allowRtCodes.length > 0"
              class="inline-block p-0.5 max-h-5 bg-blue-300 rounded-sm"
              :title="$t('driverForms.allowedExitCode')"
            >
              <OneTwoThreeIcon></OneTwoThreeIcon>
            </span>
          </div>
        </div>
      </div>

      <!-- <table class="table-fixed w-full text-sm text-left text-gray-500">
        <thead class="sticky top-0 text-xs text-gray-700 uppercase bg-gray-50">
          <tr>
            <th scope="col" class="px-4 py-4">
              {{ $t('driverForms.name') }}
            </th>
            <th scope="col" class="px-4 py-4">
              {{ $t('driverForms.path') }}
            </th>
            <th scope="col" class="sm:px-4 py-4">
              {{ $t('driverForms.argument') }}
            </th>
            <th scope="col" class="px-4 py-4">
              {{ $t('driverForms.action') }}
            </th>
          </tr>
        </thead>
        <tbody draggable="false">
          <tr
            v-for="(d, i) in driverOfType"
            :key="d.id"
            class="py-3 even:bg-half-baked-100"
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
            <td class="px-2 py-1">
              <span class="font-medium line-clamp-2 text-gray-900">
                {{ d.name }}
              </span>
            </td>
            <td class="px-2 py-1">
              <span
                class="text-xs line-clamp-3 break-all font-mono"
                :class="[
                  notExistDrivers.includes(d.id) ? 'text-rose-500 font-medium' : 'font-light'
                ]"
              >
                {{ d.path }}
              </span>
            </td>
            <td class="px-2 py-1">
              <span class="text-xs line-clamp-3">
                {{ d.flags }}
              </span>
            </td>
            <td class="px-2 py-1">
              <div class="flex gap-x-1.5">
                <button
                  class="p-1 font-medium bg-gray-200 rounded"
                  @click="$refs.inputModal?.show(d)"
                >
                  <PencilSquareIcon></PencilSquareIcon>
                </button>

                <button
                  class="p-1 font-medium bg-gray-200 rounded"
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
                  class="p-1 font-medium bg-gray-200 rounded"
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
      </table> -->
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

      <RouterLink
        :to="{ path: '/drivers/create', query: { type: driverType } }"
        class="flex items-center h-8 px-3 text-white text-sm focus:outline-none bg-powder-blue-800 hover:bg-powder-blue-700 rounded"
      >
        {{ $t('driverForms.create') }}
      </RouterLink>
    </div>
  </div>
</template>
