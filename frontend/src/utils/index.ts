import { ExecutableExists } from '@/wailsjs/go/main/App'
import type { store } from '@/wailsjs/go/models'

export function getNotExistDrivers(drivers: Array<store.Driver>) {
  return Promise.all(
    drivers.flatMap(d => ExecutableExists(d.path).then(exist => ({ id: d.id, exist: exist })))
  ).then(results => {
    return results
      .map(result => (result.exist ? undefined : result.id))
      .filter(v => v !== undefined)
  })
}
