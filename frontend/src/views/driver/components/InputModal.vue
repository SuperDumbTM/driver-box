<script setup lang="ts">
import CheckSquareIcon from '@/components/icons/CheckSquareIcon.vue'
import CrossIcon from '@/components/icons/CrossIcon.vue'
import SquareIcon from '@/components/icons/SquareIcon.vue'
import { flags } from '@/definitions/flags'
import { SelectFile } from '@/wailsjs/go/main/App'
import { store } from '@/wailsjs/go/models'
import { computed, nextTick, ref, useTemplateRef } from 'vue'
import DriverTypeBadget from './DriverTypeBadget.vue'

const props = defineProps<{ groups: Array<store.DriverGroup> }>()

const modalRef = useTemplateRef<HTMLDivElement>('modalBody')

defineExpose({
  show: (data?: Partial<store.Driver>) => {
    show.value = true

    nextTick(() => {
      modalRef.value?.scrollTo({ top: 0, behavior: 'smooth' })
    })

    if (data) {
      dri.value = {
        ...dri.value,
        ...data,
        flags: data.flags?.join(','),
        allowRtCodes: data.allowRtCodes?.join(',')
      }
    } else {
      dri.value = { minExeTime: 5, incompatibles: [] }
    }
  },
  hide: () => {
    show.value = false
  }
})

const emit = defineEmits<{
  submit: [dri: store.Driver]
}>()

const show = ref(false)

const search = ref('')

const dri = ref<
  Partial<Omit<store.Driver, 'allowRtCodes' | 'flags'> & { allowRtCodes: string; flags: string }>
>({})

const filterGroups = computed(() => {
  if (search.value === '') {
    return props.groups
  } else {
    return props.groups?.filter(
      g => g.name.includes(search.value) || g.drivers.some(d => d.name.includes(search.value))
    )
  }
})
</script>

<template>
  <Transition name="modal">
    <div class="bg-gray-900/50 fixed inset-0 z-40" v-show="show"></div>
  </Transition>

  <Transition name="modal">
    <div
      class="fixed top-0 right-0 left-0 z-50 flex justify-center items-center w-full h-full"
      v-show="show"
    >
      <div class="w-[80vw] max-w-[650px] max-h-full p-4">
        <!-- Modal content -->
        <div class="bg-white rounded-lg shadow">
          <!-- Modal header -->
          <div class="flex items-center justify-between px-3 py-1.5 border-b rounded-t bg-white">
            <h3 class="font-semibold">
              {{ dri ? $t('driverForms.editDriver') : $t('driverForms.createDriver') }}
            </h3>
            <button
              type="button"
              class="inline-flex justify-center items-center h-8 w-8 ms-auto text-sm text-gray-400 hover:text-gray-900 bg-transparent hover:bg-gray-200 rounded-lg"
              @click="
                () => {
                  show = false
                  dri = { minExeTime: 5 }
                }
              "
            >
              <CrossIcon></CrossIcon>
            </button>
          </div>

          <!-- Modal body -->
          <div class="max-h-[70vh] overflow-auto py-2 px-4" id="debug" ref="modalBody">
            <form
              class="flex flex-col gap-y-3"
              @submit.prevent="
                _ => {
                  emit(
                    'submit',
                    new store.Driver({
                      ...dri,
                      flags: dri.flags ? dri.flags.split(',') : [],
                      allowRtCodes: dri.allowRtCodes
                        ? dri.allowRtCodes
                            ?.split(',')
                            .map(c => parseInt(c))
                            .filter(c => !Number.isNaN(c))
                        : [],
                      incompatibles: dri.incompatibles ?? []
                    })
                  )
                }
              "
            >
              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.name') }}
                </label>
                <input
                  type="text"
                  name="name"
                  v-model="dri.name"
                  class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                  autocomplete="off"
                />
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.path') }}
                </label>

                <div class="flex">
                  <button
                    type="button"
                    class="w-28 px-3 text-sm text-gray-900 bg-gray-200 border border-e-0 rounded-s-md rounded-e-0 border-gray-300"
                    @click="
                      SelectFile(true).then(path => {
                        dri.path = path
                      })
                    "
                  >
                    {{ $t('driverForms.selectFile') }}
                  </button>
                  <input
                    type="text"
                    name="path"
                    v-model="dri.path"
                    class="block flex-1 min-w-0 w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 border rounded-none rounded-e-lg shadow-sm"
                    ref="pathInput"
                    autocomplete="off"
                    required
                  />
                </div>
              </div>

              <div>
                <label class="block mb-2 text-sm font-medium text-gray-900">
                  {{ $t('driverForms.argument') }}
                </label>

                <div class="flex">
                  <select
                    name="flags"
                    class="w-28 text-sm border border-e-0 rounded-e-0 rounded-s-lg border-apple-green-600 outline-none"
                    @change="
                      event => {
                        dri.flags = (event.target as HTMLSelectElement).value
                      }
                    "
                  >
                    <option value="">
                      {{ $t('driverForms.manualInput') }}
                    </option>
                    <option
                      v-for="(flag, name) in flags"
                      :key="name"
                      :value="flag.join(',')"
                      :selected="dri.flags === flag.join()"
                    >
                      {{ name }}
                    </option>
                  </select>
                  <input
                    type="text"
                    name="flags"
                    v-model="dri.flags"
                    class="block flex-1 min-w-0 w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 border rounded-none rounded-e-lg shadow-sm"
                    autocomplete="off"
                  />
                </div>

                <p class="mt-1 text-xs font-light text-apple-green-800">
                  {{ $t('driverForms.commaSeparated') }}
                </p>
              </div>

              <div class="flex gap-x-3">
                <div>
                  <label class="block mb-2 text-sm font-medium text-gray-900">
                    {{ $t('driverForms.minExecuteTime') }}
                  </label>
                  <input
                    type="number"
                    name="minExeTime"
                    v-model="dri.minExeTime"
                    step="0.1"
                    class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                    autocomplete="off"
                    required
                  />
                  <p class="mt-1 text-xs font-light text-apple-green-800">
                    {{ $t('driverForms.minExecuteTimeHelp') }}
                  </p>
                </div>

                <div>
                  <label class="block mb-2 text-sm font-medium text-gray-900">
                    {{ $t('driverForms.allowedExitCode') }}
                  </label>
                  <input
                    type="text"
                    name="allowRtCodes"
                    v-model="dri.allowRtCodes"
                    class="w-full p-1.5 text-sm border border-apple-green-600 focus:outline-powder-blue-700 rounded-lg shadow-sm"
                    autocomplete="off"
                  />
                  <p class="mt-1 text-xs font-light text-apple-green-800">
                    {{ $t('driverForms.allowedExitCodeHelp') }}
                  </p>
                  <p class="mt-1 text-xs font-light text-apple-green-800">
                    {{ $t('driverForms.commaSeparated') }}
                  </p>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-900">
                  {{ $t('driverForms.incompatibleWith') }}
                </label>

                <div class="mb-2 text-xs line-clamp-1">
                  <span class="inline">
                    {{ $t('driverForms.selectedWithCount', { count: dri.incompatibles?.length }) }}
                  </span>
                </div>

                <div class="flex mb-2 gap-x-2">
                  <input
                    v-model="search"
                    :placeholder="$t('driverForms.search')"
                    class="px-3 py-2 w-full text-black text-sm border-none rounded outline-apple-green-600 bg-gray-50"
                  />

                  <button
                    type="button"
                    class="px-3 text-sm font-medium text-white bg-powder-blue-800 hover:bg-powder-blue-600 rounded-lg"
                    :title="$t('driverForms.selectAll')"
                    @click="
                      () => {
                        dri.incompatibles = [
                          ...props.groups.flatMap(g => g.drivers.flatMap(d => d.id)),
                          'set_password',
                          'create_partition'
                        ]
                      }
                    "
                  >
                    <CheckSquareIcon></CheckSquareIcon>
                  </button>

                  <button
                    type="button"
                    class="px-3 text-sm font-medium text-white bg-rose-400 hover:bg-rose-300 rounded-lg"
                    :title="$t('driverForms.selectNone')"
                    @click="
                      () => {
                        dri.incompatibles = []
                      }
                    "
                  >
                    <SquareIcon></SquareIcon>
                  </button>
                </div>

                <ul class="h-48 p-1.5 overflow-auto bg-white border rounded-lg">
                  <li
                    class="py-2.5 px-4 text-sm"
                    v-show="
                      search === '' ||
                      'set password'.includes(search) ||
                      $t('installOptions.setPassword').includes(search)
                    "
                  >
                    <label class="flex item-center w-full select-none cursor-pointer">
                      <input
                        type="checkbox"
                        value="set_password"
                        v-model="dri.incompatibles"
                        class="me-1.5"
                      />
                      <span
                        class="content-center me-1 px-1.5 h-5 text-xs text-nowrap bg-orange-200 rounded"
                      >
                        {{ $t('driverForms.default') }}
                      </span>
                      {{ $t('installOptions.setPassword') }}
                    </label>
                  </li>

                  <li
                    class="py-2.5 px-4 text-sm"
                    v-show="
                      search === '' ||
                      'create partition'.includes(search) ||
                      $t('installOptions.createPartition').includes(search)
                    "
                  >
                    <label class="flex item-center w-full select-none cursor-pointer">
                      <input
                        type="checkbox"
                        value="create_partition"
                        v-model="dri.incompatibles"
                        class="me-1.5"
                      />
                      <span
                        class="content-center me-1 px-1.5 h-5 text-xs text-nowrap bg-orange-200 rounded"
                      >
                        {{ $t('driverForms.default') }}
                      </span>
                      {{ $t('installOptions.createPartition') }}
                    </label>
                  </li>

                  <template v-for="g in filterGroups" :key="g.id">
                    <template v-for="d in g.drivers.filter(d => d.id != dri.id)" :key="d.id">
                      <li class="py-2.5 px-4 text-sm">
                        <label class="flex items-center w-full select-none cursor-pointer">
                          <input
                            type="checkbox"
                            :value="d.id"
                            v-model="dri.incompatibles"
                            class="me-1.5"
                          />
                          <DriverTypeBadget :type="g.type"></DriverTypeBadget>
                          <span class="line-clamp-2">
                            {{ `[${g.name}] ${d.name}` }}
                          </span>
                        </label>
                      </li>
                    </template>
                  </template>
                </ul>
              </div>

              <button
                type="submit"
                class="w-full my-1 py-2 text-sm font-medium text-white bg-half-baked-600 hover:bg-half-baked-500 rounded-lg"
              >
                {{ $t('save') }}
              </button>
            </form>
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

label:has(+ input:required, + select:required):after,
label:has(+ div > input:required):after {
  content: ' *';
  color: red;
}
</style>
