describe("filterList() tests", function() {
  //--- Document Tests ---//
  beforeAll(function () {
    // Set up initial state before running the tests
    CURRENCY_LIST = ['United States Dollar', 'Euro', 'British Pound', 'Japanese Yen'];
  });
  
  it("should correctly filter the currency list for different input strings", function () {
    // Test cases for filtering the currency list based on input strings
    const inputString1 = 'United States Dollar';
    const inputString2 = 'united states dollar';
    const inputString3 = 'Dollar';
    const inputString4 = 'un';
    const inputString5 = 'uNiTeD';
    
    // Expectations
    expect(filterList(inputString1)).toContain('United States Dollar');
    expect(filterList(inputString2)).toContain('United States Dollar');
    expect(filterList(inputString3)).toContain('United States Dollar');
    expect(filterList(inputString4)).toContain('United States Dollar');
    expect(filterList(inputString5)).toContain('United States Dollar');
  });

  it("should throw error for non-string input", function() {
    const inputString1 = null;
    const inputString2 = 123;
    const inputObj = new Object;

    expect(() => filterList(inputString1)).toThrowError("Cannot read properties of null (reading 'toLowerCase')");
    expect(() => filterList(inputString2)).toThrowError("str.toLowerCase is not a function");
    expect(() => filterList(inputObj)).toThrowError("str.toLowerCase is not a function");
  });

  it("should return an empty array for non-existing input", function() {
    const inputString3 = 'Non-Existing Currency';
    expect(filterList(inputString3)).toEqual([]);
  });

  it("should handle leading and trailing whitespaces", function() {
    const inputString4 = '     united     ';
    expect(filterList(inputString4)).toEqual([]);
  });

});

describe("renderListInDropdown() tests", function() {
  let ulElement;

  beforeEach(function () {
    ulElement = document.createElement('ul');
  });

  it("should render list items in the dropdown", function () {
    const listJSON = ['Item 1', 'Item 2', 'Item 3'];
    renderListInDropdown(listJSON, ulElement);

    expect(ulElement.innerHTML).toBe('<li>Item 1</li><li>Item 2</li><li>Item 3</li>');
  });

  it("should handle an empty list", function () {
    const emptyListJSON = [];
    renderListInDropdown(emptyListJSON, ulElement);

    expect(ulElement.innerHTML).toBe('');
  });
  
  it("should handle special characters in list items", function () {
    const specialCharsListJSON = ['Item 1', '<script>alert("XSS");</script>', 'Item 3'];
    renderListInDropdown(specialCharsListJSON, ulElement);

    expect(ulElement.innerHTML).toContain('<script>alert("XSS");</script>');
  });
});

describe("noEnter() tests", function() {
  beforeEach(function() {
    // Set up a mock window.event with keyCode 13 before each test
    window.event = undefined;
  });

  it("should return true when event is not present", function() {
    expect(noEnter()).toBe(true);
  });

  it("should return true when event is present, but keyCode is not 13", function() {
    const mockEvent = { keyCode: 27 };  // Example keyCode other than 13
    window.event = mockEvent;
    expect(noEnter()).toBe(true);
  });

  it("should return false when event is present and keyCode is 13", function() {
    const enterEvent = { keyCode: 13 };
    window.event = enterEvent;
    expect(noEnter()).toBe(false);
  });

  afterEach(function() {
    // Clean up the mock window.event after each test
    window.event = undefined;
  });
});

describe("containsUppercase() tests", function() {
  it("should return true when the string contains all uppercase letters", function() {
    expect(containsUppercase("HELLO")).toBe(true);
    expect(containsUppercase("UPPERCASE")).toBe(true);
  });

  it("should return false when the string contains at least one lowercase letter", function() {
    expect(containsUppercase("Hello")).toBe(false);
    expect(containsUppercase("lowercase")).toBe(false);
    expect(containsUppercase("test123")).toBe(false);
  });

  it("should return false when the string is empty", function() {
    expect(containsUppercase("")).toBe(false);
  });

  it("should return false when the string contains numbers, symbols, or spaces", function() {
    expect(containsUppercase("TEST123")).toBe(false);
    expect(containsUppercase("12345")).toBe(false);
    expect(containsUppercase("!@#$")).toBe(false);
    expect(containsUppercase("with space")).toBe(false);
  });

  it("should return false when the input is not a string", function() {
    expect(containsUppercase(123)).toBe(false);
    expect(containsUppercase(true)).toBe(false);
    expect(containsUppercase(null)).toBe(false);
  });
});

describe("getQuoteForCurrency() tests", function() {
  // Set up for testing
  beforeAll(function () {
    // Mock data setup before running the tests
    QUOTES['USDAMD'] = 402.989408;
    QUOTES['USDMXN'] = 17.588702;
    QUOTES['USDCAD'] = 1.37955;
    CURRENCY_LIST.push('Armenian Dram');
    CURRENCY_LIST.push('Mexican Peso');
    CURRENCY_LIST.push('Canadian Dollar');
  });

  it("should return the correct conversion rate for USD", function() {
    expect(getQuoteForCurrency('USD')).toBe(1);
    expect(getQuoteForCurrency('United States Dollar')).toBe(1);
  });

  it("should return the correct conversion rate for other currencies", function() {
    expect(getQuoteForCurrency('Armenian Dram')).toEqual(402.989408);
    expect(getQuoteForCurrency('Mexican Peso')).toBe(17.588702);
    expect(getQuoteForCurrency('Canadian Dollar')).toBe(1.37955);
  });

  it("should handle unknown currencies and return undefined", function() {
    expect(getQuoteForCurrency('XXX')).toBeUndefined();
    expect(getQuoteForCurrency('monopoly money')).toBeUndefined();
    expect(getQuoteForCurrency('Canadian Dolar')).toBeUndefined();
  });

  it("should handle lowercase input for known currencies", function() {
    expect(getQuoteForCurrency('usdamd')).toBeUndefined();
    expect(getQuoteForCurrency('mexican peso')).toBeUndefined();
    expect(getQuoteForCurrency('Canadian dollar')).toBeUndefined();
  });

  it("should handle empty input and return undefined", function() {
    expect(getQuoteForCurrency('')).toBeUndefined();
  });

  it("should handle non-string input and return undefined", function() {
    expect(getQuoteForCurrency(123)).toBeUndefined();
    expect(getQuoteForCurrency(true)).toBeUndefined();
    expect(getQuoteForCurrency(null)).toBeUndefined();
  });
});
