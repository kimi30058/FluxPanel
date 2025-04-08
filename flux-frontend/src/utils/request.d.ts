import { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

declare const service: AxiosInstance;

export function download(url: string, params: any, filename: string, config?: AxiosRequestConfig): Promise<void>;

export let isRelogin: { show: boolean };

export default service;
