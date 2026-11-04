document.addEventListener('DOMContentLoaded', () => {
    const STORAGE_KEY = 'generatedColorFields_v21';

    const enableCheckbox = document.getElementById('enable-generator');
    const generatorPanel = document.getElementById('generator-panel');
    const btnAddElement = document.getElementById('btn-add-element');
    const container = document.getElementById('generated-container');

    let savedData = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];

    function saveToStorage() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(savedData));
    }

    function createElementBlock(data) {
        const block = document.createElement('div');
        block.className = 'gen-block';
        block.dataset.id = data.id;

        const colorInput = document.createElement('input');
        colorInput.type = 'color';
        colorInput.className = 'gen-color-input';
        colorInput.value = data.value || '#000000'; 
        
        if (data.name) colorInput.setAttribute('name', data.name);
        if (data.list) colorInput.setAttribute('list', data.list);
        colorInput.disabled = data.disabled;
        block.appendChild(colorInput);

        const nameWrap = document.createElement('label');
        nameWrap.className = 'gen-attr';
        nameWrap.textContent = 'name';
        const nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.value = data.name || '';
        nameInput.addEventListener('input', (e) => {
            data.name = e.target.value;
            if (data.name) colorInput.setAttribute('name', data.name);
            else colorInput.removeAttribute('name');
            saveToStorage();
        });
        nameWrap.appendChild(nameInput);
        block.appendChild(nameWrap);

        const valueWrap = document.createElement('label');
        valueWrap.className = 'gen-attr';
        valueWrap.textContent = 'value';
        const valueInput = document.createElement('input');
        valueInput.type = 'color';
        valueInput.value = data.value || '#000000';
        valueInput.disabled = data.disabled;
        valueInput.addEventListener('input', (e) => {
            data.value = e.target.value;
            colorInput.value = data.value; 
            saveToStorage();
        });
        valueWrap.appendChild(valueInput);
        block.appendChild(valueWrap);

        colorInput.addEventListener('input', (e) => {
            data.value = e.target.value;
            valueInput.value = data.value; 
            saveToStorage();
        });

        const listWrap = document.createElement('label');
        listWrap.className = 'gen-attr';
        listWrap.textContent = 'list';
        const listInput = document.createElement('input');
        listInput.type = 'text';
        listInput.value = data.list || '';
        listInput.addEventListener('input', (e) => {
            data.list = e.target.value;
            if (data.list) colorInput.setAttribute('list', data.list);
            else colorInput.removeAttribute('list');
            saveToStorage();
        });
        listWrap.appendChild(listInput);
        block.appendChild(listWrap);

        const disabledWrap = document.createElement('label');
        disabledWrap.className = 'gen-attr-checkbox';
        const disabledInput = document.createElement('input');
        disabledInput.type = 'checkbox';
        disabledInput.checked = data.disabled;
        disabledInput.addEventListener('change', (e) => {
            data.disabled = e.target.checked;
            colorInput.disabled = data.disabled; 
            valueInput.disabled = data.disabled;
            saveToStorage();
        });
        disabledWrap.appendChild(disabledInput);
        disabledWrap.appendChild(document.createTextNode('disabled'));
        block.appendChild(disabledWrap);

        const btnDelete = document.createElement('button');
        btnDelete.className = 'btn-delete-gen';
        btnDelete.textContent = 'Delete';
        btnDelete.addEventListener('click', () => {
            block.remove(); 
            savedData = savedData.filter(item => item.id !== data.id); 
            saveToStorage();
        });
        block.appendChild(btnDelete);

        return block;
    }

    function renderAll() {
        container.innerHTML = '';
        savedData.forEach(data => {
            container.appendChild(createElementBlock(data));
        });
    }

    
    enableCheckbox.addEventListener('change', (e) => {
        if (e.target.checked) {
            generatorPanel.classList.remove('hidden');
        } else {
            generatorPanel.classList.add('hidden');
        }
    });

    btnAddElement.addEventListener('click', () => {
        const newData = {
            id: Date.now().toString(), 
            name: '',
            value: '#e63946', 
            list: '',
            disabled: false
        };
        savedData.push(newData);
        saveToStorage(); 
        
        const newBlock = createElementBlock(newData);
        container.appendChild(newBlock);
    });

    renderAll();
});