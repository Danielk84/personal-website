export default interface BasePagination<T>{
  count: number;
  previous?: string | null;
  next?: string | null;
  results: T[];
}