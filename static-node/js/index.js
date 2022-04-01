
const date_element = document.getElementById('date');
const time_interval = 1000;
const diff_iteration_max = 100;

function clock_function(){
    let time = new Date();
    let count = 0;

    let update_time = () => {
        if (count >= diff_iteration_max) {
            // time difference is about 1 secound
            time = new Date();
            count = 0;
        } else {
            date_element.textContent = time.toLocaleString('ja');
            time.setTime(time.getTime() + time_interval);
            count += 1;
        }
    };

    update_time();

    setInterval(update_time, time_interval);
};

window.onload = () => {
    clock_function();
}
