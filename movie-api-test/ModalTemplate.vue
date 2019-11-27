<template>
  <div
    class="modal fade"
    tabindex="-1"
    role="dialog"
    v-bind:id="`gg-${movie.id}`"
    data-backdrop="static"
    data-keypress="false"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content bg-dark text-white">
        <div class="modal-header">
          <h5 class="modal-title">🎬 {{movie.title}} ({{movie.title_en}})</h5>
          <button type="button" class="close text-white" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <!-- Image -->
          <div>
            <img
              class="movie--poster my-3"
              v-bind:src="movie.poster_url"
              v-bind:alt="movie.title"
              style="width:50%"
            />
          </div>

          <hr style="background-color:white">

          <!-- Detail -->
          <div>
            <p class="text-center">DETAIL</p>
            <div class="mb-1">평점 : {{movie.score}}</div>
            <div class="mb-1">등급 : {{movie.grade.name}}</div>
            <div class="mb-1">
              <span>장르 : </span>
              <span v-for="(genre, index) in movie.movie_genres" :key="genre.id">
              <span v-if="index !== movie.movie_genres.length-1"> {{genre.name}},</span>
              <span v-else> {{genre.name}}</span>
            </span>
            </div>
            <div class="mb-1">
              <span>감독 : </span>
              <span v-for="(director, index) in movie.movie_directors" :key="director.id">
              <span v-if="index !== movie.movie_directors.length-1"> {{director.name}},</span>
              <span v-else> {{director.name}}</span>
            </span>
            </div>
            <div class="mb-1">누적 관람객 : {{Number(movie.audience).toLocaleString()}}명</div>
            <div class="mb-1">
              <div>줄거리</div>
              <p>{{movie.summary}}</p>
            </div>
          </div>

          <hr style="background-color:white">

          <!-- 예고편 -->
          <div>
            <p class="text-center">예고편</p>
            <span v-if="movie.video_url">
              <iframe :src="movie.video_url" frameborder="0" style="width:100% ;height:300px;"></iframe>
            </span>
            <span v-else>😱</span>
          </div>

          <!-- OST -->
          <div>
            <hr style="background-color:white">
            <p class="text-center">OST</p>
            <span v-if="movie.ost_url">
              <iframe :src="movie.ost_url" frameborder="0" style="width:100% ;height:300px;"></iframe>
            </span>
            <span v-else>😱</span>
          </div>

          <hr style="background-color:white">

          <!-- Create Review -->
          <div>
            <p class="text-center">CREATE REVIEW</p>
            <span v-if="isAuthenticated">
              <div class="row">
                <div class="col-2">
                  <label for="comment" class="p-2">comment</label>
                </div>
                <div class="input-group col">
                  <input id="comment" class="form-control" type="text" v-model="review.comment" />
                </div>
                <div class="col-1"></div>
              </div>
              
              <div class="row">
                <div class="col-2">
                  <label for="score" class="p-2">score</label>
                </div>
                <div class="input-group col">
                  <input id="score" class="form-control" type="number" v-model="review.score" />
                </div>
                <div class="col-3">
                  <button class="btn btn-primary" @click="createreview">리뷰생성</button>
                </div>
                <div class="col-1"></div>
              </div>
            </span>
            <span v-else>로그인 후 볼 수 있습니다.</span>
          </div>

          <!-- Review -->
          <!-- <div v-if="reviews.data !== []"> -->
          <div>
            <hr style="background-color:white">
            <p class="text-center">REVIEW</p>
            <div class="text-left">
              <div class="row">
                <div class="col-2">
                  user
                </div>
                <div class="col-2">
                  score
                </div>
                <div class="col">
                  comment
                </div>
                <div class="col-4"></div>
              </div>
            </div>
            <hr style="background-color:white; opacity: 0.25">
            <div v-for="review in reviews" :key="review.id" class="my-3">
              <div v-if="review.movie === movie.id" class="text-left">
                <div class="row">
                  <div class="col-2">
                    {{review.review_user.username}}
                  </div>
                  <div class="col-2">
                    {{review.score}}
                  </div>
                  <div class="col">
                    {{review.comment}}
                  </div>
                  <div v-if="review.review_user.username === userName" class="col-4">
                    <button class="btn btn-sm btn-success ml-3 mr-1" @click="updatereview(review)">수정</button>
                    <button class="btn btn-sm btn-danger" @click="deletereview(review)">삭제</button>
                  </div>
                  <!-- <div v-else class="col-4"></div> -->
                </div>
              </div>
            </div>
          </div>
          <!-- </div> -->
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jwtDecode from "jwt-decode"
import axios from "axios";
export default {
  name: "movielistitemmodal",
  props: {
    movie: Object,
    genres: Array
  },
  data() {
    return {
      review: {
        comment: "",
        score: "",
      },
      isAuthenticated: this.$session.has("jwt"),
      reviews: [],
      userName: ""
    };
  },
  methods: {
    getUserName(){
      this.$session.start()
      const token = this.$session.get("jwt")
      // console.log(typeof(token))
      if (typeof(token) === "undefined") {
        this.userName = ""
      } else {
        const decodedToken = jwtDecode(token)
        this.userName = decodedToken.username
      }
    },
    createreview() {
      const token = this.$session.get("jwt");
      const header = {
        headers: {
          Authorization: `JWT ${token}`
        }
      };
      axios
        .post(
          `http://127.0.0.1:8000/api/v1/movies/${this.movie.id}/reviews/`,
          this.review,
          header
        )
        .then(response => {
          const data = response.data;
          console.log(data);
          this.reviews.push(data);
          console.log(this.reviews);
        })
        .catch(error => {
          console.log(error);
        });
    },

    deletereview: function(review) {
      const token = this.$session.get("jwt");
      const header = {
        headers: {
          Authorization: `JWT ${token}`
        }
      };
      axios
        .delete(
          `http://127.0.0.1:8000/api/v1/movies/reviews/${review.id}/`,
          header
        )
        .then(() => {
          const targetreview = this.reviews.find(function(el) {
            return el === review;
          });
          const idx = this.reviews.indexOf(targetreview);
          if (idx > -1) {
            this.reviews.splice(idx, 1);
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    update: function(data) {
      console.log(data);
      this.comment = data.comment;
      this.score = data.score;
    },
    updatereview: function(review) {
      const token = this.$session.get("jwt");
      const header = {
        headers: {
          Authorization: `JWT ${token}`
        }
      };
      axios
        .put(
          `http://127.0.0.1:8000/api/v1/movies/reviews/${review.id}/`,
          this.review,
          header
        )
        .then(response => {
          console.log(response);
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  // watch: {
  //   reviews
  // },
  mounted() {
    this.getUserName(),
    axios
      .get(`http://127.0.0.1:8000/api/v1/movies/reviews/`)
      .then(res => {
        console.log(res.data);
        this.reviews = res.data;
      })
      .catch(err => console.log(err));
  }
};
</script>

<style>
</style>