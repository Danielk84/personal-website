import type BaseResponseData from "../interfaces/BaseResponseData";

const baseBackendURL = "/api";

export async function getStaticData<T>(
  url: string, method = "GET", timeout = 3000,
): Promise<BaseResponseData<T>> {
  try {
    const response = await fetch(baseBackendURL + url,
      {
        method: method,
        signal: AbortSignal.timeout(timeout),
        headers: { "Content-Type": "application/json" }
      },
    );
    if (!response.ok)
      throw { statusCode: response.status, msg: response.statusText };

    const json = await response.json();

    return { json: json, statusCode: response.status};
  } catch (error: any) {
    const statusCode = error?.statusCode || 404;
    const msg = error?.msg || "Page Not Found";

    return { json: {}, statusCode, msg };
  }
}