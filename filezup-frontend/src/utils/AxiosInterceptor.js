import axiosInstance from './AxiosInstance.js';

const setupAxiosInterceptor = (navigate) => {
    axiosInstance.interceptors.request.use(
        async (config) => {
            const accessToken = localStorage.getItem('userAuthentication')
                ? JSON.parse(localStorage.getItem('userAuthentication'))
                      .access_token
                : null;

            if (accessToken) {
                config.headers['Authorization'] = `Bearer ${accessToken}`;
            }

            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    axiosInstance.interceptors.response.use(
        (response) => response,
        async (error) => {
            const originalRequest = error.config;

            if (error.response.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;

                const refreshToken = localStorage.getItem('userAuthentication')
                    ? JSON.parse(localStorage.getItem('userAuthentication'))
                          .refresh_token
                    : null;

                if (refreshToken) {
                    try {
                        const response = await axiosInstance.post(
                            '/token/refresh/',
                            { refresh: refreshToken }
                        );
                        const access = response.data.access;
                        const user_details = JSON.parse(
                            localStorage.getItem('userAuthentication')
                        );
                        user_details.access_token = access;

                        localStorage.setItem(
                            'userAuthentication',
                            JSON.stringify(user_details)
                        );

                        originalRequest.headers['Authorization'] =
                            `Bearer ${access}`;
                        console.log('Doing');

                        return axiosInstance(originalRequest);
                    } catch (refreshError) {
                        localStorage.removeItem('userAuthentication');
                        navigate('/login');
                        return Promise.reject(refreshError);
                    }
                } else {
                    localStorage.removeItem('userAuthentication');
                    navigate('/login');
                }
            }

            return Promise.reject(error);
        }
    );
};

export default setupAxiosInterceptor;
