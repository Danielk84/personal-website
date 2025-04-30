import type BaseResponseData from "../interfaces/BaseResponseData";

const baseBackendURL = "/api";

export async function fetchStaticData<T>(
  url: string, method:string = "GET", data?: any, statusCode:number = 200, authToken?: string, timeout=4000,
): Promise<BaseResponseData<T>> {
  try {
    const fetchOptions: RequestInit = {
      method,
      signal: AbortSignal.timeout(timeout),
      headers: {
        "Content-Type": "application/json",
        "Authorization": authToken || "",
      }
    };

    if (["POST", "PUT", "PATCH"].includes(method) && data)
      fetchOptions.body = data;

    const response = await fetch(baseBackendURL + url, fetchOptions);
    if (!response.ok && response.status !== statusCode) throw response;
    
    const json = await response.json();
    return { json: json, statusCode: response.status};
  } catch (error: any) {
    const statusCode = error?.status || 404;
    const msg = error?.statusText || "Page Not Found";

    return { json: {} as T,statusCode, msg };
  }
}