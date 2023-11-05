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

export function wagers() {
    return api.getWagersWagersGet();
}

export function newWager(startX: number, startY: number, endX: number, endY: number, bet: number, duration: number, stream: string) {
    return api.makeWagerWagersPost({ wagerCreate: { startX, startY, endX, endY, bet, duration, stream }});
}

export function notifications() {
    return api.getNotificationsNotificationsGet();
}

export function users() {
    return api.readUsersUsersGet();
}