export type Command = {
  id: string
  name?: string
  groupName: string
  config: {
    program: string
    options: Array<string>
    minExeTime: number
    allowRtCodes: Array<number>
    incompatibles: Array<string>
  }
}

export type Process = {
  command: Command
  status:
    | 'pending'
    | 'running'
    | 'aborting'
    | 'completed'
    | 'failed'
    | 'aborted'
    | 'speeded'
    | 'broken'
  procId?: string
  result?: {
    lapse: number
    exitCode: number
    stdout: string
    stderr: string
    error: string
    aborted: boolean
  }
}
