import { Configuration, DefaultApi, type User, type UserCreate, type UserLogin } from "./generated/openapi";

const configuration = new Configuration({
    basePath: '/api',
});

const api = new DefaultApi(configuration);

export function login(username: string, password: string) {
    return api.loginLoginPost({ userLogin: { username, password } });
}

export function register(username: string, password: string) {
    return api.createUserUsersPost({ userCreate: { username, password }})
}

export function self() {
    return api.getSelfSelfGet();
}

export function logout() {
    return api.logoutLogoutPost();
}

export function streams() {
    return api.getStreamsStreamsGet();
}