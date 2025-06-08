console.log("Welcome to To-Do App");

let doneBtns = document.querySelectorAll("#done");
let deleteBtns = document.querySelectorAll("#delete");

for (let donebtn of doneBtns) {
    donebtn.addEventListener("click", function () {
        let taskContainer = this.closest(".task");
        let task = taskContainer.querySelector(".task-name");
        task.classList.add("complete-task");
        console.log(task);
    })
};

for (let deletebtn of deleteBtns) {
    deletebtn.addEventListener("click", function () {
        let taskContainer = this.closest(".task");
        let task = taskContainer.querySelector(".task-name");
        let taskIndex = Number(task.id);
        fetch(`/delete/${taskIndex}`, {
            method: "POST"
        });
        taskContainer.remove();
        console.log(task);
    })
}

