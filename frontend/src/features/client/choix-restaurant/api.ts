import { apiClient } from "../../../lib/api";
import type { Restaurant } from "../../../types/restaurant";

export const listerRestaurants = () =>
  apiClient
    .get<Restaurant[]>("/restaurants/")
    .then((response) => response.data);
