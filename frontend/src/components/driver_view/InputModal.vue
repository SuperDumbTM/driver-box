<script setup lang="ts">
import { ref, watch } from 'vue'
import CrossIcon from '../icons/CrossIcon.vue'

defineExpose({
  openModal: () => {
    show.value = true
  }
})

const show = ref(false)
</script>

<template>
  <Transition name="modal">
    <div class="bg-gray-900/50 fixed inset-0 z-40" v-show="show"></div>
  </Transition>

  <Transition name="modal">
    <div
      class="flex fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"
      v-show="show"
    >
      <div class="relative p-4 w-full max-w-md max-h-full">
        <!-- Modal content -->
        <div class="relative max-h-[80vh] overflow-y-auto bg-white rounded-lg shadow">
          <!-- Modal header -->
          <div class="flex items-center justify-between p-3 border-b rounded-t">
            <h3 class="font-semibold">新增軀動程式</h3>
            <button
              type="button"
              class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm h-8 w-8 ms-auto inline-flex justify-center items-center"
              @click="show = false"
            >
              <CrossIcon></CrossIcon>
            </button>
          </div>

          <!-- Modal body -->
          <div class="py-2 px-4">
            <form class="flex flex-col gap-y-3">
              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900"> 軀動類別 </label>
                <select
                  class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                >
                  <option value="network">有線網絡介面卡</option>
                  <option value="display">顯示卡</option>
                  <option value="miscellaneous">其他</option>
                </select>
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900"> 軀動名稱 </label>
                <input
                  type="text"
                  class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                  required
                />
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">軀動路徑</label>
                <input
                  type="file"
                  class="w-full text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm file:bg-gray-50 file:border-0 file:me-3 file:p-2 file:pe-3"
                />
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">安裝參數</label>

                <div class="grid grid-cols-4 gap-2">
                  <div class="col-span-1">
                    <select
                      class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                    >
                      <option>手動輸入</option>
                      <option>Nvidia</option>
                      <option>AMD</option>
                      <option>Intel Chipset</option>
                    </select>
                  </div>
                  <div class="col-span-3">
                    <input
                      type="text"
                      class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                      required
                    />
                  </div>
                </div>
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">執行時間（秒）</label>
                <input
                  type="number"
                  class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                  value="5"
                  required
                />
                <p class="mt-1 text-xs text-apple-green-800">
                  安裝軀動的時間少於所輸入的時間，將會被視作安裝失敗。
                </p>
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">非錯誤狀態代碼</label>
                <input
                  type="text"
                  class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                  required
                />
                <p class="mt-1 text-xs text-apple-green-800">
                  安裝程序返回所輸入的狀態代碼時，將會視作安裝成功。
                </p>
              </div>
            </form>
          </div>

          <!-- Modal footer -->
          <div class="flex items-center justify-between p-4 gap-x-4">
            <button
              class="text-white inline-flex w-full justify-center bg-blue-500 hover:bg-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
            >
              儲存
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.5s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
