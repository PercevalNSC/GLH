
const date_element = document.getElementById('date');
const time_interval = 1000;

window.onload = () => {
    let time = new Date();
    let date_text = date.toLocaleString('ja');
    date_element.textContent = date_text;

    function update_time() {
        time.setTime(time.getTime() + time_interval);
        let date_text = time.toLocaleString('ja');
        date_element.textContent = date_text;
        //console.log(date_text);
    }

    setInterval(update_time, time_interval);
}


