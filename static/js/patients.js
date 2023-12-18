function fetchPatients() {
  fetch("/api/patients/")
    .then((response) => response.json())
    .then((data) => {
      const patientsList = document.getElementById("patients-list");
      patientsList.innerHTML = ""; // Очистить текущий список
      data.forEach((patient) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${patient.full_name}`;
        listItem.className = "patient";
        listItem.id = patient.id;
        listItem.addEventListener("click", fetchPatientDetails);
        patientsList.appendChild(listItem);
      });
    })
    .catch((error) => {
      console.error("Ошибка при получении списка пациентов:", error);
    });
}

fetchPatients();

function fetchPatientDetails(event) {
  const patient_id = event.srcElement.attributes["id"];
  console.log(patient_id.value);
  fetch(`/api/patient/${patient_id.value}`)
    .then((response) => response.json())
    .then((patient) => {
      document.title = patient.full_name;
      document.body.innerHTML = "";
      const h1 = document.createElement("h1");
      h1.textContent = `${patient.full_name}`;
      const gender = document.createElement("div");
      gender.textContent = `Пол: ${patient.gender}`;
      const testsLists = document.createElement("ul");
      console.log(patient.medical_test);
      patient.medical_test.forEach((test) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${test.test_date} - ${test.test_name}`;
        listItem.addEventListener("click", () => {
          showMedicalTestDetail(patient, test);
        });
        testsLists.appendChild(listItem);
      });
      document.body.appendChild(h1);
      document.body.appendChild(gender);
      document.body.appendChild(testsLists);
    })
    .catch((error) => {
      console.error("Ошибка при получении списка анализов:", error);
    });
}

function showMedicalTestDetail(patient, test) {
  document.title = test.test_date;
  document.body.innerHTML = "";
  const h1 = document.createElement("h1");
  h1.textContent = `${test.test_date} - ${test.test_name}`;
  document.body.appendChild(h1);
  const patientInfo = document.createElement("div");
  patientInfo.className = "patient-info";
  const name = document.createElement("div");
  name.textContent = `Имя: ${patient.full_name}`;
  patientInfo.appendChild(name);
  const gender = document.createElement("div");
  gender.textContent = `Пол: ${patient.gender}`;
  patientInfo.appendChild(gender);
  const age = document.createElement("div");
  age.textContent = `Возраст: ${test.age}`;
  patientInfo.appendChild(age);
  const testDate = document.createElement("div");
  testDate.textContent = `Дата взятия образца: ${test.test_date}`;
  patientInfo.appendChild(testDate);
  const table = document.createElement("table");
  const tableTitle = document.createElement("thead");
  const titleRow = document.createElement("tr");
  const researchName = document.createElement("th");
  researchName.textContent = "Исследование";
  const researchValue = document.createElement("th");
  researchValue.textContent = "Результат";
  const researchUnits = document.createElement("th");
  researchUnits.textContent = "Единицы";
  titleRow.appendChild(researchName);
  titleRow.appendChild(researchValue);
  titleRow.appendChild(researchUnits);
  tableTitle.appendChild(titleRow);
  table.appendChild(tableTitle);
  const tbody = document.createElement("tbody");
  for (let [key, value] of Object.entries(test.researches)) {
    let tRow = document.createElement("tr");
    let rowItem = document.createElement("td");
    rowItem.textContent = `${key}`;
    let rowItem2 = document.createElement("td");
    rowItem2.textContent = `${value["result"]}`;
    let rowItem3 = document.createElement("td");
    rowItem3.textContent = `${value["units"]}`;
    tRow.appendChild(rowItem);
    tRow.appendChild(rowItem2);
    tRow.appendChild(rowItem3);
    tbody.appendChild(tRow);
  }
  table.appendChild(tbody);
  document.body.appendChild(patientInfo);
  document.body.appendChild(table);
}