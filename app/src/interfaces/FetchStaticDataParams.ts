export default interface FetchStaticDataParams {
  url: string;
  method?:string;
  data?: any;
  statusCode?:number;
  authToken?: string;
  timeout?: number;
}