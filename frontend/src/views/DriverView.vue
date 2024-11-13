<script setup lang="ts">
import InputModal from '@/components/driver_view/InputModal.vue'
import PencilSquareIcon from '@/components/icons/PencilSquareIcon.vue'
import TrashIcon from '@/components/icons/TrashIcon.vue'
import * as manager from '@/wailsjs/go/store/DriverManager'
import { store } from '@/wailsjs/go/models'
import { ref } from 'vue'
import CopyIcon from '@/components/icons/CopyIcon.vue'

const driType = ref(store.DriverType.NETWORK)
const drivers = ref<Array<store.Driver> | null>(null)

manager.Read().then(d => {
  drivers.value = d
})
</script>

<template>
  <div class="flex flex-col h-full gap-y-3">
    <ul class="flex flex-row gap-x-3 list-none text-center">
      <li class="flex-1">
        <a
          class="block px-4 py-3 text-xs leading-normal font-bold uppercase select-none shadow-lg rounded"
          :class="{
            'text-half-baked-600 bg-white': driType !== store.DriverType.NETWORK,
            'text-white bg-half-baked-600': driType === store.DriverType.NETWORK
          }"
          @click="driType = store.DriverType.NETWORK"
        >
          有線網絡介面卡
        </a>
      </li>
      <li class="flex-1">
        <a
          class="block px-4 py-3 text-xs leading-normal font-bold uppercase select-none shadow-lg rounded"
          :class="{
            'text-half-baked-600 bg-white': driType !== store.DriverType.DISPLAY,
            'text-white bg-half-baked-600': driType === store.DriverType.DISPLAY
          }"
          @click="driType = store.DriverType.DISPLAY"
        >
          顯示卡
        </a>
      </li>
      <li class="flex-1">
        <a
          class="block px-4 py-3 text-xs leading-normal font-bold uppercase select-none shadow-lg rounded"
          :class="{
            'text-half-baked-600 bg-white': driType !== store.DriverType.MISCELLANEOUS,
            'text-white bg-half-baked-600': driType === store.DriverType.MISCELLANEOUS
          }"
          @click="driType = store.DriverType.MISCELLANEOUS"
        >
          其他
        </a>
      </li>
    </ul>

    <div class="flex flex-col grow min-h-48 overflow-y-auto shadow-lg rounded">
      <table class="table-fixed text-sm text-left text-gray-500">
        <thead class="sticky top-0 text-xs text-gray-700 uppercase bg-gray-50">
          <tr>
            <th scope="col" class="px-4 py-4 text-nowrap">軀動名稱</th>
            <th scope="col" class="px-4 py-4 text-nowrap">路徑</th>
            <th scope="col" class="sm:px-4 py-4 text-nowrap">安裝參數</th>
            <th scope="col" class="px-4 py-4 text-nowrap">動作</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="d in drivers?.filter(d => d.type == driType)"
            :key="d.id"
            class="bg-white border-b"
          >
            <th scope="row" class="px-4 py-2 text-sm font-medium text-gray-900 whitespace-nowrap">
              {{ d.name }}
            </th>
            <td class="px-4 py-2 min-w-28 text-xs break-all">{{ d.path }}</td>
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

    <div class="flex justify-end">
      <button
        type="button"
        class="h-8 px-3 text-white text-sm focus:outline-none bg-powder-blue-800 hover:bg-powder-blue-600 rounded"
        @click="$refs.inputModal?.show({ type: driType })"
      >
        新增
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
