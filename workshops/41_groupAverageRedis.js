import { check, sleep } from "k6";
import http from "k6/http";

export default function() {
    let random = Math.floor(Math.random() * 3) + 1  
    let res = http.get("http://query_service_redis/average-speed-group/"+random);
    check(res, {
        "is status 200": (r) => r.status === 200
    });
    sleep(1);
};
