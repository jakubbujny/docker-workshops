import { check, sleep } from "k6";
import http from "k6/http";

export default function() {
    let res = http.get("http://query_service/average-speed/882");
    check(res, {
        "is status 200": (r) => r.status === 200
    });
    sleep(1);
};
