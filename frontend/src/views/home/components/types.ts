export type Command = {
  id: string
  procId?: string
  name: string
  status:
    | 'pending'
    | 'running'
    | 'aborting'
    | 'completed'
    | 'failed'
    | 'aborted'
    | 'speeded'
    | 'broken'
  program: string
  options: Array<string>
  minExeTime: number
  allowRtCodes: Array<number>
  incompatibles: Array<string>
  result?: {
    lapse: number
    exitCode: number
    stdout: string
    stderr: string
    error: string
    aborted: boolean
  }
}
