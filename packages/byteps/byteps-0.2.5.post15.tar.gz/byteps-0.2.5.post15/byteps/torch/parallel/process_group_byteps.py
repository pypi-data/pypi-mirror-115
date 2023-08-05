class ProcessGroupBYTEPS(ProcessGroup):
    class WorkBYTEPS(ProcessGroup.Work):
        def __init__(self, devices):
            devices_ = []
            blockingWait_ = False
            store_ = None
            xxx
        def isCompleted(self):
            xxx
        def isSuccess(self):
            xxx
        def wait(self):
            xxx
        def abort(self):
            xxx
        def synchronize(self):
            xxx
        def finishedGPUExecution():
            xxx

    def __init__(
        prefix_store,
        rank,
        world_size,
        timeout):
        blockingWait = os.environ.get('BYTEPS_BLOCKING_WAIT', '0')
        val = int(blockingWait)
        if val == 1:
            blockingWait_ = True
        elif val != 0:
            raise RuntimeError("Invalid value for environment variable: " +
                    blockingWait)


