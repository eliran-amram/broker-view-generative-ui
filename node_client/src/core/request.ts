/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { AxiosInstance, AxiosPromise } from "axios";
import type { ApiRequestOptions } from "./ApiRequestOptions";

const isDefined = <T>(
  value: T | null | undefined
): value is Exclude<T, null | undefined> => {
  return value !== undefined && value !== null;
};

const getQueryString = (params: Record<string, any>): string => {
  const qs: string[] = [];

  const append = (key: string, value: any) => {
    qs.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`);
  };

  const process = (key: string, value: any) => {
    if (isDefined(value)) {
      if (Array.isArray(value)) {
        value.forEach((v) => {
          process(key, v);
        });
      } else if (typeof value === "object") {
        Object.entries(value).forEach(([k, v]) => {
          process(`${key}[${k}]`, v);
        });
      } else {
        append(key, value);
      }
    }
  };

  Object.entries(params).forEach(([key, value]) => {
    process(key, value);
  });

  if (qs.length > 0) {
    return `?${qs.join("&")}`;
  }

  return "";
};

const getUrl = (withPrefix: boolean, prefix: string, options: ApiRequestOptions): string => {
  const initialUrl = options.url;
  const urlWithPrecidingSlash = initialUrl.startsWith('/') ? initialUrl : '/' + initialUrl;
  const urlWithOptionalPrefix = withPrefix && prefix ? prefix + urlWithPrecidingSlash : urlWithPrecidingSlash;
  const url = urlWithOptionalPrefix
    .replace("{api-version}", "1.0.0")
    .replace(/{(.*?)}/g, (substring: string, group: string) => {
      if (options.path?.hasOwnProperty(group)) {
        return encodeURI(String(options.path[group]));
      }
      return substring;
    });

  if (options.query) {
    return `${url}${getQueryString(options.query)}`;
  }
  return url;
};

export const request = <T>(
  axiosInstance: AxiosInstance,
  withPrefix: boolean,
  prefix: string,
  options: ApiRequestOptions
): AxiosPromise<T> => {
  const url = `${getUrl(withPrefix, prefix, options)}`;

  const formData = options.formData;
  const fromDataObject = new FormData();
  if (formData) {
    Object.entries(formData).forEach(([key, value]) => {
      fromDataObject.append(key, value);
    });
  }

  return axiosInstance.request({
    url,
    data: options.body ? options.body : options.formData ? fromDataObject : undefined,
    method: options.method,
  });
}
