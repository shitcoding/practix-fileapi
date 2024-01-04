TEST_PERSON_DATA_INDEX = [
    {
        "uuid": "6c83581b-03ae-4f6a-84f2-d946c3e5b981",
        "full_name": "Rabindranath Tagore"
    },
    {
        "uuid": "6c961189-7f16-4938-96cc-7a034547dded",
        "full_name": "Dushyanth Weeraman"
    },
    {
        "uuid": "6c9ae6e9-43c3-4d5c-b857-49c26c61ffba",
        "full_name": "Chihiro Suzuki"
    }
]

TEST_PERSON_DATA = [
    {
        "uuid": "6c83581b-03ae-4f6a-84f2-d946c3e5b981",
        "full_name": "Rabindranath Tagore",
        "films": [
            {
                "uuid": "6fddb231-8127-42f0-81e5-f53a806c2ae8",
                "roles": [
                    "writer"
                ]
            }
        ]
    },
    {
        "uuid": "6c961189-7f16-4938-96cc-7a034547dded",
        "full_name": "Dushyanth Weeraman",
        "films": [
            {
                "uuid": "72900b34-4169-451b-a896-2a16844eac7b",
                "roles": [
                    "actor"
                ]
            }
        ]
    },
    {
        "uuid": "6c9ae6e9-43c3-4d5c-b857-49c26c61ffba",
        "full_name": "Chihiro Suzuki",
        "films": [
            {
                "uuid": "c20959d2-daca-4cb2-a104-e1ab63479da3",
                "roles": [
                    "actor"
                ]
            }
        ]
    }
]

TEST_FILM = [{
    "uuid": "72900b34-4169-451b-a896-2a16844eac7b",
    "imdb_rating": 5,
    "title": "Dancing Star",
    "description": "",
    "file_path": "",
    "genre": [
        {
            "uuid": "9c91a5b2-eb70-4889-8581-ebe427370edd",
            "name": "Musical"
        },
        {
            "uuid": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
            "name": "Romance"
        }
    ],
    "directors": [
        {
            "uuid": "b2d686a6-f029-41c3-ad9e-fc586117866a",
            "full_name": "Susara Dinal"
        }
    ],
    "actors": [
        {
            "uuid": "6c961189-7f16-4938-96cc-7a034547dded",
            "full_name": "Dushyanth Weeraman"
        },
        {
            "uuid": "fbedcdd1-74b4-42f8-a04c-4f2dc212f1c0",
            "full_name": "Shiroshi Romeshika"
        },
        {
            "uuid": "00ead298-388c-4a94-8969-553e8096f2c6",
            "full_name": "Srilal Ahangama"
        },
        {
            "uuid": "c15fdba0-6afe-472e-96f6-8c22afd8c04c",
            "full_name": "Malini Fonseka"
        }
    ],
    "writers": []
},
    {
        "uuid": "c20959d2-daca-4cb2-a104-e1ab63479da3",
        "imdb_rating": 7.2,
        "title": "Voices of a Distant Star",
        "description": "The story of the high school students Mikako Nagamine and Noboru Terao. When the alien "
                       "Tarsians attack, Mikako volunteers to be a pilot in the space force that will protect "
                       "mankind. The lovers try to remain in contact using cellular telephone text messages, "
                       "but as each battle takes Mikako further from the Earth, each message takes longer to arrive. "
                       "Will their love stand the tests of time and distance?",
        "genre": [
            {
                "uuid": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
                "name": "Romance"
            },
            {
                "uuid": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395",
                "name": "Short"
            },
            {
                "uuid": "1cacff68-643e-4ddd-8f57-84b62538081a",
                "name": "Drama"
            },
            {
                "uuid": "6a0a479b-cfec-41ac-b520-41b2b007b611",
                "name": "Animation"
            },
            {
                "uuid": "6c162475-c7ed-4461-9184-001ef3d9f26e",
                "name": "Sci-Fi"
            }
        ],
        "directors": [],
        "actors": [
            {
                "uuid": "74a4e5ce-5fa7-4f62-aad6-7b529e0cd96e",
                "full_name": "Makoto Shinkai"
            },
            {
                "uuid": "6c9ae6e9-43c3-4d5c-b857-49c26c61ffba",
                "full_name": "Chihiro Suzuki"
            },
            {
                "uuid": "ab890976-8022-464a-ad14-35de35bee244",
                "full_name": "Mika Shinohara"
            },
            {
                "uuid": "f12a07e5-6da5-4c16-8b0f-c42f7b13c52f",
                "full_name": "Sumi Mutoh"
            }
        ],
        "writers": []
    }
]

FILMS_OF_PERSON = [
    {
        "uuid": "c20959d2-daca-4cb2-a104-e1ab63479da3",
        "title": "Voices of a Distant Star",
        "imdb_rating": 7.2
    }
]
