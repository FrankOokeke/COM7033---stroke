/**
 * Attach click event to all Edit buttons.
 * Extract patient data from data attribute and populate the form.
 */
document.addEventListener('DOMContentLoaded', () => {
    const editButtons = document.querySelectorAll('.edit-button');

    editButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Parse the patient data from the button's data attribute
            const patient = JSON.parse(button.getAttribute('data-patient'));

            // Populate the form fields with patient data
            document.getElementById('action').value = 'edit';
            document.getElementById('id').value = patient.id;
            document.getElementById('gender').value = patient.gender;
            document.getElementById('age').value = patient.age;
            document.getElementById('hypertension').value = patient.hypertension;
            document.getElementById('heart_disease').value = patient.heart_disease;
            document.getElementById('ever_married').value = patient.ever_married;
            document.getElementById('work_type').value = patient.work_type;
            document.getElementById('Residence_type').value = patient.Residence_type;
            document.getElementById('avg_glucose_level').value = patient.avg_glucose_level;
            document.getElementById('bmi').value = patient.bmi;
            document.getElementById('smoking_status').value = patient.smoking_status;
        });
    });
});