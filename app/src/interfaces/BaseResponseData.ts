export default interface BaseResponseData<T> {
  json: T | Object;
  statusCode: number;
  msg?: string;
}