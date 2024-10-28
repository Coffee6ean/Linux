const fs = require('fs');
const dbSeed = require('/home/coffee_6ean/Linux/AdvancedModels/src/backend/seeds/POC/dbTables.js');
const dbSimulation = require('/home/coffee_6ean/Linux/AdvancedModels/src/backend/seeds/POC/dbSimulation.json')

// Create a JSON file to store the data
const jsonSeed = JSON.stringify(dbSeed);
const jsonSimulation = JSON.stringify(dbSimulation);

// Seed data to the JSON file
function seed() {
  return fs.writeFileSync("dbSimulation.json", jsonSeed);
}

// Implement CRUD operations
function create(table, data) {
  // Create a new record in the database
  dbObj = JSON.parse(jsonSimulation);
  const tableTemp = dbObj.tables.find((element) => element.name == table);
  if(data.id > 0) {
    if(tableTemp.values[tableTemp.values.length - 1].id >= data.id) {
      console.log('Error: record already exists');
      console.log("//------------------------//");
      return 'Error: record already exists';
    } else {
      tableTemp.values.push(data);
      return fs.writeFileSync("dbSimulation.json", JSON.stringify(dbObj));
    }
  }

  console.log('Error: Indexing issues. Out of bounds');
  console.log("//------------------------//");
  return 'Error: Indexing issues. Out of bounds';
}

function read (table, id) {
  // Find a record in the database
  dbObj = JSON.parse(jsonSimulation);
  for(let tableTemp of dbObj.tables) {
    if(tableTemp.name == table) {
      if(id <= 0) {
        console.log('Error: Indexing issue. Out of bounds');
        console.log("//------------------------//");
        return 'Error: Indexing issue. Out of bounds';
      }
      let record = tableTemp.values[id - 1] ? tableTemp.values[id - 1] : 'Error: id not found in specified table';
      console.log(record);
      console.log("//------------------------//");
      return record;
    }
  }
  return false;
}

function update(table, id, data) {
  // Update a record in the database
  dbObj = JSON.parse(jsonSimulation);
  const tableTemp = dbObj.tables.find((element) => element.name == table);
  for(let record of tableTemp.values) {
    if(record.id == id) {
      Object.assign(record, data);
      return fs.writeFileSync("dbSimulation.json", JSON.stringify(dbObj));
    }
    if(record.id > id) {
      console.log('Error: id not found in specified table');
      console.log("//------------------------//");
      break;
    }
  }

  console.log('Error: id not found in specified table');
  console.log("//------------------------//");
  return 'Error: id not found in specified table';
}

function remove(table, id) {
  // Delete a record from the database
  dbObj = JSON.parse(jsonSimulation);
  const tableTemp = dbObj.tables.find((element) => element.name == table);
  const record = tableTemp.values.find((record) => record.id === id);
  tableTemp.values.splice(tableTemp.values.indexOf(record), 1);
  return fs.writeFileSync("dbSimulation.json", JSON.stringify(dbObj));
}

if (require.main === module) {
  //seed();
  
  //const newRecord = { ...data };
  /*
  create('users', {
    "id": 11,
    "username": "devTester1",
    "password": "devtest_101",
    "email": "devTester@example.com",
    "first_name": "Jhonny",
    "sur_name": "JB",
    "last_name": "Bones",
    "birth_date": "2000-01-01",
    "about": "Software engineer :]",
    "pronouns": "he/him",
    "website": null,
    "linked_in": null,
    "role": "Software Engineer",
    "profession": "Software Development",
    "team_id": 1,
    "created_at": Date.now(),
    "updated_at": Date.now()
  });
  read('projects', 4);
  read('users', 10);
  read('users', 11);
  */
  /*
  update('users', 11, {
    "website": 'www.example_domain.com',
    "linked_in": 'www.linkedin.com/in/dev-tester/',
    "updated_at": Date.now()
  });
  */
  remove('users', 11);
}