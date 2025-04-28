export default interface BaseResponseData<T> {
  json?: T;
  statusCode: number;
  msg?: string;
}