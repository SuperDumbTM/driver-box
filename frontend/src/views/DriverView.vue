<script setup lang="ts">
import InputModal from '@/components/driver_view/InputModal.vue'
import { ref } from 'vue'

const driverType = ref('newtowk')
</script>

<template>
  <div class="flex flex-col h-full gap-y-3">
    <ul class="flex flex-row gap-x-3 list-none text-center">
      <li class="flex-1">
        <a
          class="block px-4 py-3 text-xs leading-normal font-bold uppercase shadow-lg rounded"
          :class="{
            'text-half-baked-600 bg-white': driverType !== 'newtowk',
            'text-white bg-half-baked-600': driverType === 'newtowk'
          }"
          @click="driverType = 'newtowk'"
        >
          有線網絡介面卡
        </a>
      </li>
      <li class="flex-1">
        <a
          class="block px-4 py-3 text-xs leading-normal font-bold uppercase shadow-lg rounded"
          :class="{
            'text-half-baked-600 bg-white': driverType !== 'display',
            'text-white bg-half-baked-600': driverType === 'display'
          }"
          @click="driverType = 'display'"
        >
          顯示卡
        </a>
      </li>
      <li class="flex-1">
        <a
          class="block px-4 py-3 text-xs leading-normal font-bold uppercase shadow-lg rounded"
          :class="{
            'text-half-baked-600 bg-white': driverType !== 'miscellaneous',
            'text-white bg-half-baked-600': driverType === 'miscellaneous'
          }"
          @click="driverType = 'miscellaneous'"
        >
          其他
        </a>
      </li>
    </ul>

    <div class="flex flex-col grow min-h-48 overflow-y-auto shadow-lg rounded">
      <table class="text-sm text-left text-gray-500">
        <thead class="sticky top-0 text-xs text-gray-700 uppercase bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3">軀動名稱</th>
            <th scope="col" class="px-6 py-3">路徑</th>
            <th scope="col" class="px-6 py-3">安裝參數</th>
            <th scope="col" class="px-6 py-3">動作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in 2" :key="i" class="bg-white border-b">
            <th scope="row" class="px-5 py-3 font-medium text-gray-900 whitespace-nowrap">
              Apple MacBook Pro 17"
            </th>
            <td class="px-5 py-3">Silver</td>
            <td class="px-5 py-3">Laptop</td>
            <td class="px-5 py-3"></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex justify-end">
      <button
        type="button"
        class="h-8 px-3 text-white text-sm focus:outline-none bg-powder-blue-800 hover:bg-powder-blue-600 rounded"
        @click="$refs.inputModal?.openModal()"
      >
        新增
      </button>
    </div>

    <InputModal ref="inputModal"></InputModal>
  </div>
</template>
