// LocalStorage Keys
const USERS_KEY = 'medconnect_pharmacies';
let activeUser = null;

// Temporary Initial Stock
let medicineInventory = [
  { id: 1, name: 'Paracetamol 500mg', qty: 45, status: 'In Stock' },
  { id: 2, name: 'Amoxicillin 250mg', qty: 4, status: 'Low Stock' }
];

// Helper: Get Saved Pharmacies
function getRegisteredPharmacies() {
  return JSON.parse(localStorage.getItem(USERS_KEY)) || [];
}

// Auth Tab Toggle
function switchAuthTab(tab) {
  const loginTab = document.getElementById('tabLogin');
  const regTab = document.getElementById('tabRegister');
  const loginForm = document.getElementById('loginForm');
  const regForm = document.getElementById('registerForm');

  if (tab === 'login') {
    loginTab.classList.add('active');
    regTab.classList.remove('active');
    loginForm.style.display = 'block';
    regForm.style.display = 'none';
  } else {
    regTab.classList.add('active');
    loginTab.classList.remove('active');
    loginForm.style.display = 'none';
    regForm.style.display = 'block';
  }
}

// View Switcher Utility
function showView(viewId) {
  document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
  document.getElementById(viewId).classList.add('active');
}

// Handle Registration
async function handleRegistration(e) {

    e.preventDefault();

    const pharmacy = {

        shop_name: document.getElementById("shopName").value,
        owner_name: document.getElementById("ownerName").value,
        phone: document.getElementById("phone").value,
        dl_number: document.getElementById("license").value,
        address: document.getElementById("address").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
        

    };


    try {

        const response = await fetch("/pharmacy/register", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(pharmacy)

        });


        const result = await response.json();


        if (response.ok) {

            alert(result.message);

            document.getElementById("registerForm").reset();

        }

        else {

            alert(result.error);

        }

    }

    catch (error) {

        console.error(error);

        alert("Unable to connect to the server.");

    }

}
  pharmacies.push(newPharmacy);
  localStorage.setItem(USERS_KEY, JSON.stringify(pharmacies));

  document.getElementById('headerPharmacyName').innerText = newPharmacy.name;
  document.getElementById('registerForm').reset();

  showView('pendingView');
}

// Handle Login
function handleLogin(e) {
  e.preventDefault();

  const email = document.getElementById('loginEmail').value.toLowerCase();
  const password = document.getElementById('loginPassword').value;

  const pharmacies = getRegisteredPharmacies();
  const foundUser = pharmacies.find(p => p.email === email && p.password === password);

  if (!foundUser) {
    alert('Invalid Email or Password. Please register first if you do not have an account.');
    return;
  }

  activeUser = foundUser;
  document.getElementById('headerPharmacyName').innerText = activeUser.name;

  if (activeUser.isApproved) {
    showDashboard();
  } else {
    showView('pendingView');
  }
}

// Display Dashboard
function showDashboard() {
  document.getElementById('dashPharmacyName').innerText = activeUser.name;
  showView('dashboardView');
  renderInventory();
}

// Render Medicine Inventory
function renderInventory() {
  const tbody = document.getElementById('inventoryTableBody');
  tbody.innerHTML = '';

  medicineInventory.forEach((item, index) => {
    let badgeClass = 'badge-instock';
    if (item.status === 'Low Stock') badgeClass = 'badge-lowstock';
    if (item.status === 'Out of Stock') badgeClass = 'badge-outstock';

    const row = document.createElement('tr');
    row.innerHTML = `
      <td><strong>${item.name}</strong></td>
      <td>${item.qty} units</td>
      <td><span class="badge ${badgeClass}">${item.status}</span></td>
      <td><button onclick="removeStock(${index})" style="color: red; border: none; background: none; cursor: pointer;">Remove</button></td>
    `;
    tbody.appendChild(row);
  });
}

// Add Stock
function addMedicineStock(e) {
  e.preventDefault();
  const name = document.getElementById('medName').value;
  const qty = document.getElementById('medQty').value;
  const status = document.getElementById('medStatus').value;

  medicineInventory.push({ id: Date.now(), name, qty, status });
  document.getElementById('stockForm').reset();
  renderInventory();
}

// Remove Stock
function removeStock(index) {
  medicineInventory.splice(index, 1);
  renderInventory();
}

// Logout
function logout() {
  activeUser = null;
  document.getElementById('headerPharmacyName').innerText = 'Guest Mode';
  document.getElementById('loginForm').reset();
  switchAuthTab('login');
  showView('authView');
}