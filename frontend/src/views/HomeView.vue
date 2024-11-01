<script setup lang="ts"></script>

<template>
  <div class="flex flex-col h-full">
    <div class="grow min-h-28 border rounded"></div>

    <hr class="my-4" />

    <div class="flex gap-x-3 h-32">
      <div class="flex flex-col flex-1 gap-y-3 justify-around">
        <div class="relative w-full">
          <select
            class="block w-full peer ps-3 pe-9 pt-5 pb-2 border-2 border-gray-200 rounded-lg focus:border-powder-blue-900"
          >
            <option>請選擇</option>
            <option>1</option>
            <option>2</option>
            <option>3</option>
          </select>
          <label
            class="absolute top-0 start-0 h-full p-4 pt-3 -translate-y-1.5 text-xs truncate text-gray-500 pointer-events-none"
          >
            網絡介面卡
          </label>
        </div>

        <div class="relative w-full">
          <select
            class="block w-full peer ps-3 pe-9 pt-5 pb-2 border-2 border-gray-200 rounded-lg focus:border-powder-blue-900"
          >
            <option>請選擇</option>
            <option>1</option>
            <option>2</option>
            <option>3</option>
          </select>
          <label
            class="absolute top-0 start-0 h-full p-4 pt-3 -translate-y-1.5 text-xs truncate text-gray-500 pointer-events-none"
          >
            顯示卡
          </label>
        </div>
      </div>

      <div class="flex flex-1">
        <div class="relative w-full h-full mb-3">
          <div class="block h-full overflow-y-scroll ps-2 pt-3 rounded border">
            <div class="flex items-center mb-1">
              <input type="checkbox" class="w-4 h-4" />
              <label class="ms-2 text-sm text-gray-900">Default checkbox</label>
            </div>
          </div>
          <label
            class="absolute left-3 top-0 w-10 origin-[0_0] -translate-y-[0.55rem] bg-white text-primary scale-[0.9] text-center text-neutral-500 truncate pointer-events-none"
          >
            其他
          </label>
        </div>
      </div>
    </div>

    <hr class="my-4" />

    <div class="flex gap-x-6">
      <div class="flex flex-col">
        <fieldset>
          <p class="font-bold">額外工作</p>

          <div class="flex gap-x-3">
            <div class="flex items-center mb-4">
              <input
                type="checkbox"
                class="text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
              />
              <label class="ms-2 text-sm">建立磁區</label>
            </div>

            <div class="flex items-center mb-4">
              <input
                type="checkbox"
                class="text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
              />
              <label class="ms-2 text-sm">設定密碼</label>
            </div>
          </div>
        </fieldset>

        <fieldset>
          <p class="font-bold">安裝設定</p>

          <div class="flex gap-x-3">
            <div class="flex items-center mb-4">
              <input
                type="checkbox"
                class="text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
              />
              <label class="ms-2 text-sm">同步安裝</label>
            </div>
          </div>
        </fieldset>
      </div>

      <div class="flex flex-col grow justify-between">
        <fieldset class="w-full">
          <label class="block mb-1 text-sm font-bold text-gray-900">關機設定</label>
          <select class="block w-full p-1 text-sm text-gray-900 border border-gray-300 rounded-lg">
            <option>請選擇</option>
            <option value="none">沒有動作</option>
            <option value="shutdown">關機</option>
            <option value="reboot">重新開機</option>
            <option value="firmware">進入 BIOS/UEFI</option>
          </select>
        </fieldset>

        <div class="flex flex-row gap-x-2 justify-end items-center">
          <button
            type="button"
            class="h-8 px-3 text-white text-sm bg-rose-700 hover:bg-rose-600 rounded"
          >
            重置輸入
          </button>
          <button
            type="button"
            class="h-8 px-3 text-white text-sm focus:outline-none bg-half-baked-600 hover:bg-half-baked-500 rounded"
          >
            執行
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
