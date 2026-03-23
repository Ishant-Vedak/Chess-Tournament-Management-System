const csvInput = document.getElementById("csv-input")
const inputForm = document.getElementById('input-group')
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
const uploadURL = inputForm.dataset.url
console.log(uploadURL)
csvInput.addEventListener('change', ()=>{
    if(csvInput.files[0]){
        console.log(csvInput.files[0])
        const formData = new FormData()
        formData.append('csv_file', csvInput.files[0])

        fetch(uploadURL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
        .then(response => {
            response.json()
            console.log(response)
        })
        .then(data => {
            console.log(data)
            if (data.success) {
                csvInput.value = ''
            }else{
                console.error('Data was not sent successfully.')
            }
        })
        .catch(error => {
            console.error('Error:', error)   
        })
    }
})