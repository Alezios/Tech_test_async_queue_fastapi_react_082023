const delayedRequests: Map<string, () => void | Promise<void>> = new Map();
const delayedRequestsHasTimout: Map<string, boolean> = new Map();

export const delayRequest = (
  key: string,
  request: () => void | Promise<void>,
  options: { timeout: number; doInitialCall: boolean } = {
    timeout: 1000,
    doInitialCall: true,
  }
) => {
  if (!delayedRequestsHasTimout.has(key)) {
    delayedRequestsHasTimout.set(key, true);
    if (options.doInitialCall) request();
    else delayedRequests.set(key, request);
    setTimeout(() => {
      const request = delayedRequests.get(key);
      delayedRequestsHasTimout.delete(key);
      request &&
        delayRequest(key, request, { ...options, doInitialCall: true });
      delayedRequests.delete(key);
    }, options.timeout);
  } else {
    delayedRequests.set(key, request);
  }
};
