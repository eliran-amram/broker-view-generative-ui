/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import { request as __request } from '../core/request';
import { AxiosInstance, AxiosPromise } from 'axios';

export class DefaultService {
    httpClient: AxiosInstance;
    prefix: string;
    constructor(httpClient: AxiosInstance, prefix = '') {
        this.httpClient = httpClient;
        this.prefix = prefix;
    }

    /**
     * Chat With Bot
     * @returns any Successful Response
     * @throws ApiError
     */
    public chatWithBot(withPrefix = true): AxiosPromise<any> {
        return __request<any>(this.httpClient, withPrefix, this.prefix, {
            method: 'POST',
            url: '/bot/chat',
        });
    }

    /**
     * Health Check
     * @returns any Successful Response
     * @throws ApiError
     */
    public healthCheckHealthCheckGet(withPrefix = true): AxiosPromise<any> {
        return __request<any>(this.httpClient, withPrefix, this.prefix, {
            method: 'GET',
            url: '/health_check',
        });
    }

}
