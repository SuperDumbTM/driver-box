import type { Process } from './types'

export function getProcessName(process: Process) {
  return process.command.name
    ? `${process.command.groupName} - ${process.command.name}`
    : process.command.groupName
}
