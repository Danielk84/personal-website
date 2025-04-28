import type BasePagination from "../interfaces/BasePagination";

type Pagination<T> = BasePagination<T> | T[];

export declare function Paginate<T = Object>(data: BasePagination<T>): BasePagination<T>;

export function checkPagination<T = Object>(data: Object): Pagination<T> {
  if ("results" in data) {
    return data as BasePagination<T>;
  }
  return data as T[];
}