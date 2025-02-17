DROP TABLE tblMark;

DROP TABLE tblLesson;

DROP TABLE tblSubject;

DROP TABLE tblTeacher;

DROP TABLE tblPupil;

CREATE TABLE tblTeacher (
 -- Идентификатор учителя
    intTeacherId INT NOT NULL PRIMARY KEY IDENTITY (1, 1),
 -- ФИО учителя
    txtTeacherName NVARCHAR(150) NOT NULL,
 -- Год принятия на работу
    intTeacherYear INT NOT NULL,
 -- Оклад
    fltTeacherSalary DECIMAL NOT NULL,
);

CREATE TABLE tblSubject (
 -- Идентификатор предмета
    intSubjectId INT NOT NULL PRIMARY KEY IDENTITY (1, 1),
 -- Название предмета
    txtSubjectName NVARCHAR(20) NOT NULL,
 -- Количество часов
    intSubjectVolume INT NOT NULL,
 -- Учитель, ведущий занятия по предмету
    intTeacherId INT NOT NULL FOREIGN KEY REFERENCES tblTeacher(intTeacherId) ON UPDATE CASCADE ON DELETE NO ACTION,
 -- Количество проведенных уроков
    intLessonCount INT NOT NULL,
);

CREATE TABLE tblPupil (
 -- Идентификатор ученика
    intPupilId INT NOT NULL PRIMARY KEY IDENTITY (1, 1),
 -- Фамилия ученика
    txtPupilSurname NVARCHAR(30) NOT NULL,
 -- Имя ученика
    txtPupilName NVARCHAR(25) NOT NULL,
 -- Дата рождения
    datBirthday DATE NOT NULL,
 -- Пол
    chrPupilSex NVARCHAR(1) NOT NULL,
 -- Адрес проживания
    txtAddress NVARCHAR(100) NOT NULL,
);

CREATE TABLE tblLesson (
 -- Идентификатор урока
    intLessonId INT NOT NULL PRIMARY KEY IDENTITY (1, 1),
 -- Предмет
    intSubjectId INT NOT NULL FOREIGN KEY REFERENCES tblSubject(intSubjectId) ON UPDATE CASCADE ON DELETE NO ACTION,
 -- Дата проведения урока
    datLessonDate DATE NOT NULL,
 -- Тема урока
    txtTheme NVARCHAR(100) NOT NULL,
);

CREATE TABLE tblMark (
 -- Идентификатор записи об оценке
    intMarkId INT NOT NULL PRIMARY KEY IDENTITY (1, 1),
 -- Урок
    intLessonId INT NOT NULL FOREIGN KEY REFERENCES tblLesson(intLessonId) ON UPDATE CASCADE ON DELETE NO ACTION,
 -- Ученик
    intPupilId INT NOT NULL FOREIGN KEY REFERENCES tblPupil(intPupilId) ON UPDATE CASCADE ON DELETE NO ACTION,
 -- Оценка, полученная учеником на уроке
    intMarkValue INT NOT NULL,
 -- Замечания учителя
    txtMarkComment NVARCHAR(200) NOT NULL,
);

