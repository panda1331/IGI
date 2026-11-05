class ContactsTable {
    constructor() {
        this.data = [];
        this.filteredData = [];
        this.currentPage = 1;
        this.itemsPerPage = 3;
        this.sortField = 'full_name';
        this.sortAsc = true;

        this.tbody = document.getElementById('table-body');
        this.pagination = document.getElementById('table-pagination');
        this.preloader = document.getElementById('table-preloader');
        this.form = document.getElementById('add-contact-form');
        this.btnAdd = document.getElementById('btn-add-to-table');
        this.formError = document.getElementById('form-error-msg');

        this.selectedIds = new Set();
        
        this.init();
    }

    init() {
        this.showPreloader();
        this.loadData();
        this.bindEvents();
    }

    loadData() {
        this.selectedIds.clear();
        const xhr = new XMLHttpRequest();
        const self = this; 

        xhr.open('GET', '/accounts/api/contacts/', true);
        
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    const json = JSON.parse(xhr.responseText);
                    self.data = json.contacts;
                    self.applyFilter();
                } else {
                    console.error('Error loading data');
                }
                self.hidePreloader(); 
            }
        };
        
        xhr.send(null);
    }

    sortData(field) {
        if (this.sortField === field) {
            this.sortAsc = !this.sortAsc;
        } else {
            this.sortField = field;
            this.sortAsc = true;
        }
        
        this.filteredData.sort((a, b) => {
            let valA = a[field] || '';
            let valB = b[field] || '';
            if (valA < valB) return this.sortAsc ? -1 : 1;
            if (valA > valB) return this.sortAsc ? 1 : -1;
            return 0;
        });

        this.currentPage = 1;
        this.renderTable();
        this.updateSortIcons();
    }

    updateSortIcons() {
        document.querySelectorAll('.sort-icon').forEach(el => el.textContent = '');
        const activeTh = document.querySelector(`th[data-sort="${this.sortField}"] .sort-icon`);
        if (activeTh) activeTh.textContent = this.sortAsc ? '▲' : '▼';
    }

    applyFilter() {
        const search = document.getElementById('filter-input').value.toLowerCase().trim();
        
        if (!search) {
            this.filteredData = [...this.data];
        } else {
            this.filteredData = this.data.filter(item => {
                const fullName = (item.full_name || '').toLowerCase();
                const description = (item.description || '').toLowerCase();
                const phone = (item.phone || '').toLowerCase();
                const email = (item.email || '').toLowerCase();
                const website = (item.website_url || '').toLowerCase();

                return fullName.includes(search) ||
                       description.includes(search) ||
                       phone.includes(search) ||
                       email.includes(search) ||
                       website.includes(search);
            });
        }
        
        this.currentPage = 1; 
        this.sortData(this.sortField); 
    }

    renderTable() {
        this.tbody.innerHTML = '';
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        const paginatedItems = this.filteredData.slice(start, end);

        paginatedItems.forEach(item => {
            const tr = document.createElement('tr');
            tr.dataset.id = item.id;
            const isChecked = this.selectedIds.has(item.id) ? 'checked' : '';

            tr.innerHTML = `
                <td onclick="event.stopPropagation()">
                    <input type="checkbox" class="row-checkbox" value="${item.id}" ${isChecked}>
                </td>
                <td>${item.full_name}</td>
                <td>${item.description}</td>
                <td>${item.phone}</td>
                <td>${item.email}</td>
            `;

            const checkbox = tr.querySelector('.row-checkbox');
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.selectedIds.add(item.id);  
                } else {
                    this.selectedIds.delete(item.id);
                }
            });

            tr.addEventListener('click', () => this.showDetails(item));
            this.tbody.appendChild(tr);
        });

        this.renderPagination();

        const selectAllCheckbox = document.getElementById('select-all');
        if (selectAllCheckbox) {
            const currentPageCheckboxes = this.tbody.querySelectorAll('.row-checkbox');
            const checkedCheckboxes = this.tbody.querySelectorAll('.row-checkbox:checked');
            
            if (currentPageCheckboxes.length > 0 && currentPageCheckboxes.length === checkedCheckboxes.length) {
                selectAllCheckbox.checked = true;
            } else {
                selectAllCheckbox.checked = false;
            }
        }
    }

    renderPagination() {
        this.pagination.innerHTML = '';
        const totalPages = Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;

        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.textContent = i;
            if (i === this.currentPage) btn.classList.add('active');
            btn.addEventListener('click', () => {
                this.currentPage = i;
                this.renderTable();
            });
            this.pagination.appendChild(btn);
        }
    }

    showDetails(item) {
        const block = document.getElementById('row-details');
        document.getElementById('details-content').innerHTML = `
            <div class="details-text">
                <p><strong>Name:</strong> ${item.full_name}</p>
                <p><strong>Description:</strong> ${item.description}</p>
                <p><strong>Phone:</strong> ${item.phone}</p>
                <p><strong>Email:</strong> ${item.email}</p>
            </div>
            ${item.photo ? `<img src="${item.photo}" class="details-photo" alt="Photo">` : ''}
        `;
        block.classList.remove('hidden');
    }

    validateUrl(url) {
        return /^https?:\/\/.+\.(php|html)$/i.test(url);
    }

    validatePhone(phone) {
        const clean = phone.replace(/[\s()-]/g, '');
        return /^(\+375|8)0?(17|25|29|33|44)\d{7}$/.test(clean);
    }

    checkFormValidity() {
        const fields = [
            document.getElementById('new-fullname'),
            document.getElementById('new-photo'), 
            document.getElementById('new-website'),
            document.getElementById('new-description'),
            document.getElementById('new-phone'),
            document.getElementById('new-email')
        ];

        let allFilled = true;
        let allValid = true;

        fields.forEach(f => {
            if (!f.value.trim()) {
                allFilled = false;
                f.classList.remove('invalid');
            } else {
                if (f.id === 'new-website' && !this.validateUrl(f.value)) {
                    f.classList.add('invalid');
                    allValid = false;
                } else if (f.id === 'new-phone' && !this.validatePhone(f.value)) {
                    f.classList.add('invalid');
                    allValid = false;
                } else {
                    f.classList.remove('invalid');
                }
            }
        });

        if (allFilled && allValid) {
            this.formError.textContent = "All fields are valid. You can add.";
            this.formError.style.color = "green";
            this.btnAdd.disabled = false;
        } else {
            this.formError.textContent = "Fill fields correctly (URL: .html/.php, valid phone).";
            this.formError.style.color = "red";
            this.btnAdd.disabled = true;
        }
    }

    bindEvents() {
        document.querySelectorAll('th[data-sort]').forEach(th => {
            th.addEventListener('click', () => this.sortData(th.dataset.sort));
        });

        document.getElementById('btn-filter').addEventListener('click', () => this.applyFilter());

        document.getElementById('btn-open-form').addEventListener('click', () => this.form.classList.remove('hidden'));
        document.getElementById('btn-close-form').addEventListener('click', () => this.form.classList.add('hidden'));

        this.form.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', () => this.checkFormValidity());
        });

        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (this.btnAdd.disabled) return;

            const formData = new FormData();

            formData.append('full_name', document.getElementById('new-fullname').value);
            formData.append('website_url', document.getElementById('new-website').value);
            formData.append('description', document.getElementById('new-description').value);
            formData.append('phone', document.getElementById('new-phone').value);
            formData.append('email', document.getElementById('new-email').value);
            
            const fileInput = document.getElementById('new-photo');
            if (fileInput.files.length > 0) {
                formData.append('photo', fileInput.files[0]); 
            }

            this.showPreloader();
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const self = this; 

            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/accounts/api/contacts/add/', true);
            xhr.setRequestHeader('X-CSRFToken', csrfToken);

            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        const result = JSON.parse(xhr.responseText);
                        if (result.status === 'success') {
                            self.form.reset();
                            self.form.classList.add('hidden');
                            self.btnAdd.disabled = true;
                            self.loadData(); 
                        } else {
                            alert('Error: ' + result.message);
                            self.hidePreloader();
                        }
                    } else {
                        console.error('Error saving data');
                        self.hidePreloader();
                    }
                }
            };
            
            xhr.send(formData);
        });

        document.getElementById('btn-bonus').addEventListener('click', () => {
            if (this.selectedIds.size === 0) return alert('Select employees');
    
            const names = [];
            this.selectedIds.forEach(id => {
                const emp = this.data.find(d => d.id == id);
                if (emp) names.push(emp.full_name);
            });

            const bonusBlock = document.getElementById('bonus-result');
            bonusBlock.textContent = `Bonus paid to: ${names.join(', ')}`;
            bonusBlock.classList.remove('hidden');

            this.selectedIds.clear();                        
            document.querySelectorAll('.row-checkbox').forEach(cb => {
                cb.checked = false;                            
            });
            const selectAll = document.getElementById('select-all');
            if (selectAll) selectAll.checked = false;  
        });

        document.getElementById('select-all').addEventListener('change', (e) => {
            const isChecked = e.target.checked;
            document.querySelectorAll('.row-checkbox').forEach(cb => {
                cb.checked = isChecked;
                const id = parseInt(cb.value);
                if (isChecked) {
                    this.selectedIds.add(id);
                } else {
                    this.selectedIds.delete(id);
                }
            });
        });
    }

    showPreloader() { this.preloader.classList.remove('hidden'); }
    hidePreloader() { this.preloader.classList.add('hidden'); }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('table-body')) {
        new ContactsTable();
    }
});