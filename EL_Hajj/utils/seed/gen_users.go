package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"slices"
	"strconv"
	"strings"
	"time"
)

// password,last_login,email,is_email_verified,code,first_name,last_name,phone,dateOfBirth,province,gender,nombreInscription,role,winner,winning_date,personal_picture,city

type City struct {
    name string
    province int
    population int
    id int
}

func check(err error) {
    if (err != nil) {
        panic(err)
    }
}

func getFirstName(gender string) string {
    maleFirstNames := []string{ 
        "youness", "mohamed", "nadir", "abd-essamad", "abdou", "youcef", "ibrahim", "ayoub", "hamid", "yacoub",
    }
    femaleFirstNames := []string { 
        "karima", "fatima", "aicha", "aya", "meriem", "manar", "yasmine", "khalida", "asmaa", "zainab",
    }
    if (gender == "male") {
        return maleFirstNames[rand.Intn(len(maleFirstNames))];
    }
    return femaleFirstNames[rand.Intn(len(maleFirstNames))];
}

func getLastName() string {
    lastNames := []string {
        "merzouka", "rais", "chellal", "bourass", "fendi", "ameri", "boukennouche", "maredj", "krim", "hallouche", 
        "abahri", "benahmed", "hassi", "merzouk",
    }
    return lastNames[rand.Intn(len(lastNames))]
}

func getGender() string {
    if (rand.Intn(2) == 1) {
        return "M"
    }
    return "F"
}

// admin, doctor, drawing_manager, payment_manager, user, hajj
func getEmail(city City, role string, index int) string {
    cityName := strings.ToLower(city.name)
    switch role {
    case "user":
        return fmt.Sprintf("%s-user%d@gmail.com", cityName, index)
    case "hajj":
        return fmt.Sprintf("%s-hajj%d@gmail.com", cityName, index)
    case "drawingManager":
        return fmt.Sprintf("%s-drawing-manager%d@gmail.com", cityName, index)
    case "paymentManager":
        return fmt.Sprintf("%s-payment-manager%d@gmail.com", cityName, index)
    case "doctor":
        return fmt.Sprintf("%s-doctor%d@gmail.com", cityName, index)
    case "admin":
        return fmt.Sprintf("%s-admin%d@gmail.com", cityName, index)
    }
    panic("invalid role")
}

func getPhone() string {
    providers := []string{
        "5", "6", "7",
    }
    phone := fmt.Sprintf("+213-%s", providers[rand.Intn(len(providers))])
    for i := 0; i < 8; i++ {
        phone += strconv.Itoa(rand.Intn(10))
    }
    return phone
}

func getDateOfBirth() string {
    return time.Now().AddDate(-1 * (18 + rand.Intn(13)), -1 * (1 + rand.Intn(12)), -1 * (1 + rand.Intn(31))).Format("2006-01-02")
}

func getCity(cities []City) City {
    return cities[rand.Intn(len(cities))]
}

func getRole(role string) string {
    /* ("user","user"),
    ("administrateur","administrateur"),
    ("responsable tirage","responsable tirage"),
    ("medecin","medecin"),
    ("Hedj","Hedj"),
    ("banquier","banquier"), */
    switch role {
    case "user":
        return "user"
    case "admin":
        return "administrateur"
    case "drawingManager":
        return "responsable tirage"
    case "doctor":
        return "medecin"
    case "hajj":
        return "Hedj"
    case "paymentManager":
        return "banquier"
}
    panic("invalid role")
}

func genLines(role string, cities []City, number int, passwords []string, passwordBase int) []string {
    result := []string{}
    // password,email,first_name,last_name,phone,dateOfBirth,province,gender,role,city
    for i := 0; i < number; i++ {
        city := getCity(cities)
        gender := getGender()
        result = append(result, fmt.Sprintf(
            "('%s','%s','%s','%s','%s','%s',%d,'%s','%s','%s')", 
            passwords[passwordBase + i],
            getEmail(city, role, i),
            getFirstName(gender),
            getLastName(),
            getPhone(),
            getDateOfBirth(),
            city.province,
            gender,
            getRole(role),
            city.name,
        ))
    }
    return result
}

func main() {
    data, err := os.ReadFile("./passwords.txt")
    check(err)
    passwords := strings.Split(string(data), "\n")

    data, err = os.ReadFile("../cities.json")
    check(err)

    var cities []City
    err = json.Unmarshal(data, &cities)
    check(err)
    columns := "password,email,first_name,last_name,phone,dateOfBirth,province,gender,role,city"
    provinces := []int{}
    for i := 0; i < 3; i++ {
        provinces = append(provinces, rand.Intn(48))
    }
    provinceCities := []City{}
    for _, city := range cities {
        if (slices.Contains(provinces, city.province)) {
            provinceCities = append(provinceCities, city)
        }
    }
    // admin, doctor, drawing_manager, payment_manager, user, hajj
    // accounts = 1 + 10 + 10 + 10 + 50 + 35
    roleCount := map[string]int{
        "admin": 1,
        "doctor": 10,
        "drawingManager": 10,
        "paymentManager": 10,
        "user": 50,
        "hajj": 35,
    }
    lines := []string{}
    index := 0
    for role, count := range roleCount {
        lines = append(lines, genLines(role, cities, count, passwords, index)...)
    }
    table_name := "authentication_user"
    query := fmt.Sprintf("INSERT INTO %s (%s) VALUES %s;", table_name, columns, strings.Join(lines, ","))
    err = os.WriteFile("./queries/users.sql", []byte(query), 0644) 
    check(err)
}
