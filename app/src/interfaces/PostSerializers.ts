interface BasePost {
  title: string;
  slug: string;
  pub_date: string;
  user: string;

}

export interface PostOverview extends BasePost {
  summary: string;
}

export interface Post extends BasePost {
  body: string;
  last_modify: string;
}