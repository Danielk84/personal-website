export default interface BaseResponseData<T> {
  data?: T;
  statusCode: number;
  msg?: string;
}